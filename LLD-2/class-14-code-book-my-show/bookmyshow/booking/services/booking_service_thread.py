"""
Booking Service - Thread-based Locking Implementation

CONCURRENCY CONTROL: Python threading locks

Interview Points:
1. Application-level locking using threading.Lock
2. Only works for single server (not distributed)
3. Good for understanding concepts, NOT for production
4. Shows difference between app-level and DB-level locking

Pros:
- Simple to understand
- No database overhead

Cons:
- Only works in single process/server
- Doesn't scale horizontally
- Lock lost on server restart
- Not suitable for distributed systems

Interview Question: Why is this not used in production?
Answer: Modern apps run on multiple servers (horizontal scaling).
Thread locks only work within a single Python process.
User A on Server 1 and User B on Server 2 won't share the lock!

When to use:
- Educational purposes
- Understanding concurrency basics
- Small single-server applications
- Prototyping

For production distributed systems, use:
- Database locks (pessimistic)
- Version fields (optimistic)
- Distributed locks (Redis, Zookeeper)
"""
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import uuid
import threading
from collections import defaultdict

from ..models import (
    Show, ShowSeat, Ticket, TicketSeat, Payment,
    SeatStatus, TicketStatus, PaymentStatus, Coupon
)
from .base_service import BaseService


class BookingServiceThread(BaseService):
    """
    Booking service using Python thread locks

    Interview Note: This is for EDUCATIONAL purposes only!
    Do NOT use in production with multiple servers.
    """

    # Class-level lock manager
    # Interview Question: Why defaultdict(threading.Lock)?
    # Answer: Each seat gets its own lock to reduce contention
    _seat_locks = defaultdict(threading.Lock)
    _lock_manager_lock = threading.Lock()  # Lock for the lock manager itself!

    @classmethod
    def _get_seat_lock(cls, seat_id):
        """
        Get or create lock for a specific seat

        Interview Note: We need a lock to manage locks (meta-locking!)
        """
        with cls._lock_manager_lock:
            return cls._seat_locks[seat_id]

    def book_tickets(self, user, show_id, seat_ids, payment_mode, coupon_code=None):
        """
        Book tickets with thread-based locking

        Flow:
        1. Acquire locks for all seats (ordered to prevent deadlock)
        2. Validate and book
        3. Release locks

        Interview Question: Why sort seat_ids?
        Answer: To prevent deadlock. If two threads acquire locks in
        different order, they can deadlock each other.

        Example Deadlock without sorting:
        Thread A: lock(seat1) -> waiting for lock(seat2)
        Thread B: lock(seat2) -> waiting for lock(seat1)
        Both wait forever!

        Solution: Always acquire locks in same order (sorted by ID)
        """

        # Sort to prevent deadlock
        sorted_seat_ids = sorted(seat_ids)
        locks = [self._get_seat_lock(seat_id) for seat_id in sorted_seat_ids]

        # Acquire all locks in order
        # Interview Note: We acquire all locks before starting transaction
        for lock in locks:
            lock.acquire()

        try:
            # Now we have exclusive access to these seats (in this process)
            result = self._book_tickets_locked(
                user, show_id, seat_ids, payment_mode, coupon_code
            )
            return result

        finally:
            # Always release locks, even if exception occurs
            # Interview Note: Use try-finally to prevent lock leaks
            for lock in locks:
                lock.release()

    @transaction.atomic
    def _book_tickets_locked(self, user, show_id, seat_ids, payment_mode, coupon_code=None):
        """
        Actual booking logic (called while holding locks)

        Interview Note: Similar to pessimistic, but lock is in Python, not DB
        """

        # Fetch seats (no select_for_update needed, we have thread lock)
        show_seats = list(
            ShowSeat.objects.filter(
                show_id=show_id,
                id__in=seat_ids
            ).select_related('seat', 'show', 'show__movie')
        )

        if len(show_seats) != len(seat_ids):
            raise ValueError("Some seats not found")

        # Validate availability
        unavailable_seats = [
            ss.seat.number for ss in show_seats
            if ss.status != SeatStatus.AVAILABLE
        ]

        if unavailable_seats:
            raise ValueError(
                f"Seats not available: {', '.join(unavailable_seats)}"
            )

        # Validate booking time
        show = show_seats[0].show
        if not show.is_booking_allowed():
            raise ValueError("Booking cutoff time has passed")

        # Calculate amount
        total_amount = sum(ss.price for ss in show_seats)

        # Apply coupon
        discount = 0
        if coupon_code:
            discount = self._apply_coupon(coupon_code, total_amount, user)
            total_amount -= discount

        # Lock seats
        ShowSeat.objects.filter(
            id__in=[ss.id for ss in show_seats]
        ).update(
            status=SeatStatus.LOCKED,
            locked_at=timezone.now(),
            locked_by=user
        )

        # Create ticket
        ticket = Ticket.objects.create(
            id=f"TKT-{uuid.uuid4().hex[:12].upper()}",
            user=user,
            show=show,
            amount=total_amount,
            status=TicketStatus.BOOKED
        )

        # Create associations
        ticket_seats = [
            TicketSeat(ticket=ticket, show_seat=ss)
            for ss in show_seats
        ]
        TicketSeat.objects.bulk_create(ticket_seats)

        # Create payment
        payment = Payment.objects.create(
            id=f"PAY-{uuid.uuid4().hex[:12].upper()}",
            ticket=ticket,
            amount=total_amount,
            mode=payment_mode,
            status=PaymentStatus.PENDING,
            transaction_id=f"TXN-{uuid.uuid4().hex[:16].upper()}"
        )

        return {
            'ticket': ticket,
            'payment': payment,
            'total_amount': total_amount,
            'discount': discount
        }

    @transaction.atomic
    def confirm_booking(self, ticket_id, payment_success=True):
        """Confirm booking"""
        ticket = Ticket.objects.select_related('payment').get(id=ticket_id)
        payment = ticket.payment

        if payment_success:
            ShowSeat.objects.filter(
                ticket_seats__ticket=ticket
            ).update(status=SeatStatus.BOOKED)

            ticket.status = TicketStatus.CONFIRMED
            ticket.save()

            payment.status = PaymentStatus.SUCCESS
            payment.save()
        else:
            ShowSeat.objects.filter(
                ticket_seats__ticket=ticket
            ).update(
                status=SeatStatus.AVAILABLE,
                locked_at=None,
                locked_by=None
            )

            ticket.status = TicketStatus.CANCELLED
            ticket.save()

            payment.status = PaymentStatus.FAILED
            payment.save()

        return ticket

    @transaction.atomic
    def cancel_booking(self, ticket_id, user):
        """Cancel booking"""
        ticket = Ticket.objects.select_related('show', 'payment').get(id=ticket_id)

        if ticket.user != user:
            raise PermissionError("Not authorized to cancel this ticket")

        if not ticket.can_cancel():
            raise ValueError("Cannot cancel: cutoff time passed")

        ShowSeat.objects.filter(
            ticket_seats__ticket=ticket
        ).update(
            status=SeatStatus.AVAILABLE,
            locked_at=None,
            locked_by=None
        )

        ticket.status = TicketStatus.CANCELLED
        ticket.save()

        payment = ticket.payment
        payment.status = PaymentStatus.REFUNDED
        payment.save()

        return ticket

    def _apply_coupon(self, coupon_code, amount, user):
        """Apply coupon"""
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            raise ValueError("Invalid coupon code")

        if not coupon.is_valid():
            raise ValueError("Coupon is not valid or has expired")

        if amount < coupon.min_amount:
            raise ValueError(
                f"Minimum booking amount ${coupon.min_amount} required"
            )

        if coupon.discount_type == 'PERCENTAGE':
            discount = amount * (coupon.discount_value / 100)
            if coupon.max_discount:
                discount = min(discount, coupon.max_discount)
        else:
            discount = coupon.discount_value

        coupon.current_usage += 1
        coupon.save()

        return discount

    @staticmethod
    def get_available_seats(show_id):
        """Get available seats"""
        return ShowSeat.objects.filter(
            show_id=show_id,
            status=SeatStatus.AVAILABLE
        ).select_related('seat').order_by('seat__number')

    @staticmethod
    def cleanup_expired_locks():
        """Cleanup expired locks"""
        timeout = timezone.now() - timedelta(minutes=10)

        count = ShowSeat.objects.filter(
            status=SeatStatus.LOCKED,
            locked_at__lt=timeout
        ).update(
            status=SeatStatus.AVAILABLE,
            locked_at=None,
            locked_by=None
        )

        return count


"""
INTERVIEW DISCUSSION: Why Thread Locks Don't Scale

Scenario: BookMyShow in production
- Running on 10 servers for load balancing
- User A connects to Server 1
- User B connects to Server 2
- Both try to book Seat X at the same time

With Thread Locks:
- Server 1: Thread lock acquired for Seat X
- Server 2: Thread lock acquired for Seat X (different process!)
- Both proceed to book
- Result: DOUBLE BOOKING! ❌

With Database Locks (Pessimistic):
- Server 1: DB row lock on Seat X
- Server 2: Waits for lock
- Only one succeeds
- Result: Correct ✓

With Optimistic Locking:
- Server 1: Updates with version check
- Server 2: Updates with version check
- One succeeds, one fails and retries
- Result: Correct ✓

Key Insight:
- Thread locks are per-process
- Database locks are shared across all processes/servers
- For distributed systems, need shared coordination mechanism

Alternative for Distributed Systems:
1. Database locks (our pessimistic approach)
2. Distributed locks (Redis SETNX, Redlock)
3. Distributed coordination (Zookeeper, etcd)

When Thread Locks ARE Useful:
- In-memory caches (within a process)
- Background job queues (Celery with single worker)
- Protecting shared data structures (within a server)
- Educational purposes (understanding concurrency basics)
"""
