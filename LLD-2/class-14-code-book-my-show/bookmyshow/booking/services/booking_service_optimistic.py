"""
Booking Service - Optimistic Locking Implementation

CONCURRENCY CONTROL: Version-based optimistic locking

Interview Points:
1. No database locks during read
2. Version field tracks concurrent modifications
3. Update fails if version changed (retry needed)
4. Better concurrency - no blocking
5. Best for low-contention scenarios

Pros:
- Higher concurrency (non-blocking)
- Better performance for reads
- No deadlock issues
- Scales better

Cons:
- Need retry logic
- Wasted work if conflict occurs
- More complex error handling

When to use:
- Low probability of conflicts
- Read-heavy workloads
- Need high concurrency
- Can afford retry logic

Flow:
1. Read with version
2. Process data
3. Update with version check (WHERE version = old_version)
4. If rows_updated = 0, someone else modified it -> retry
"""
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
import uuid

from ..models import (
    Show, ShowSeat, Ticket, TicketSeat, Payment,
    SeatStatus, TicketStatus, PaymentStatus, Coupon
)
from .base_service import BaseService


class OptimisticLockException(Exception):
    """
    Custom exception for optimistic lock failures
    Interview Note: Use custom exceptions for specific error handling
    """
    pass


class BookingServiceOptimistic(BaseService):
    """
    Booking service using optimistic (version-based) locking
    Interview Note: Uses version field to detect concurrent modifications
    """

    MAX_RETRIES = 3  # Maximum retry attempts

    def book_tickets(self, user, show_id, seat_ids, payment_mode, coupon_code=None):
        """
        Book tickets with optimistic locking and retry logic

        Interview Question: Why do we need retry logic here?
        Answer: If version check fails, we retry with latest data
        """
        for attempt in range(self.MAX_RETRIES):
            try:
                return self._book_tickets_attempt(
                    user, show_id, seat_ids, payment_mode, coupon_code
                )
            except OptimisticLockException:
                if attempt == self.MAX_RETRIES - 1:
                    raise ValueError(
                        "Seats were modified by another user. Please try again."
                    )
                # Small delay before retry (exponential backoff)
                import time
                time.sleep(0.1 * (2 ** attempt))

        raise ValueError("Booking failed after multiple attempts")

    @transaction.atomic
    def _book_tickets_attempt(self, user, show_id, seat_ids, payment_mode, coupon_code=None):
        """
        Single attempt to book tickets

        Interview Note: Each attempt is atomic, but no locks acquired
        """

        # Step 1: Read seats WITHOUT locking (just fetch version)
        show_seats = list(
            ShowSeat.objects.filter(
                show_id=show_id,
                id__in=seat_ids
            ).select_related('seat', 'show', 'show__movie')
        )

        if len(show_seats) != len(seat_ids):
            raise ValueError("Some seats not found")

        # Step 2: Store versions for optimistic lock check
        seat_versions = {ss.id: ss.version for ss in show_seats}

        # Step 3: Validate availability (data might be stale!)
        unavailable_seats = [
            ss.seat.number for ss in show_seats
            if ss.status != SeatStatus.AVAILABLE
        ]

        if unavailable_seats:
            raise ValueError(
                f"Seats not available: {', '.join(unavailable_seats)}"
            )

        # Step 4: Validate booking time
        show = show_seats[0].show
        if not show.is_booking_allowed():
            raise ValueError("Booking cutoff time has passed")

        # Step 5: Calculate amount
        total_amount = sum(ss.price for ss in show_seats)

        # Step 6: Apply coupon
        discount = 0
        if coupon_code:
            discount = self._apply_coupon(coupon_code, total_amount, user)
            total_amount -= discount

        # Step 7: Try to update seats with version check
        # This is the CRITICAL part of optimistic locking
        updated_count = ShowSeat.objects.filter(
            id__in=seat_ids,
            status=SeatStatus.AVAILABLE
        ).update(
            status=SeatStatus.LOCKED,
            locked_at=timezone.now(),
            locked_by=user,
            version=F('version') + 1  # Increment version atomically
        )

        # Step 8: Check if update succeeded
        if updated_count != len(seat_ids):
            # Someone else modified the seats!
            # Interview Question: What happened?
            # Answer: Another transaction changed status or version
            raise OptimisticLockException("Seats were modified concurrently")

        # Alternative approach: Check each seat individually
        # for seat_id, old_version in seat_versions.items():
        #     updated = ShowSeat.objects.filter(
        #         id=seat_id,
        #         version=old_version,  # Only update if version matches
        #         status=SeatStatus.AVAILABLE
        #     ).update(
        #         status=SeatStatus.LOCKED,
        #         locked_at=timezone.now(),
        #         locked_by=user,
        #         version=F('version') + 1
        #     )
        #     if not updated:
        #         raise OptimisticLockException(f"Seat {seat_id} was modified")

        # Step 9: Create ticket (same as pessimistic)
        ticket = Ticket.objects.create(
            id=f"TKT-{uuid.uuid4().hex[:12].upper()}",
            user=user,
            show=show,
            amount=total_amount,
            status=TicketStatus.BOOKED
        )

        # Step 10: Create ticket-seat associations
        ticket_seats = [
            TicketSeat(ticket=ticket, show_seat=ss)
            for ss in show_seats
        ]
        TicketSeat.objects.bulk_create(ticket_seats)

        # Step 11: Create payment
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
        """
        Confirm booking - similar to pessimistic but with version check
        """
        ticket = Ticket.objects.select_related('payment').get(id=ticket_id)
        payment = ticket.payment

        if payment_success:
            # Update with version increment
            ShowSeat.objects.filter(
                ticket_seats__ticket=ticket
            ).update(
                status=SeatStatus.BOOKED,
                version=F('version') + 1
            )

            ticket.status = TicketStatus.CONFIRMED
            ticket.save()

            payment.status = PaymentStatus.SUCCESS
            payment.save()
        else:
            # Release seats
            ShowSeat.objects.filter(
                ticket_seats__ticket=ticket
            ).update(
                status=SeatStatus.AVAILABLE,
                locked_at=None,
                locked_by=None,
                version=F('version') + 1
            )

            ticket.status = TicketStatus.CANCELLED
            ticket.save()

            payment.status = PaymentStatus.FAILED
            payment.save()

        return ticket

    @transaction.atomic
    def cancel_booking(self, ticket_id, user):
        """Cancel booking with version-based updates"""
        ticket = Ticket.objects.select_related('show', 'payment').get(id=ticket_id)

        if ticket.user != user:
            raise PermissionError("Not authorized to cancel this ticket")

        if not ticket.can_cancel():
            raise ValueError("Cannot cancel: cutoff time passed or already cancelled")

        # Release seats with version increment
        ShowSeat.objects.filter(
            ticket_seats__ticket=ticket
        ).update(
            status=SeatStatus.AVAILABLE,
            locked_at=None,
            locked_by=None,
            version=F('version') + 1
        )

        ticket.status = TicketStatus.CANCELLED
        ticket.save()

        payment = ticket.payment
        payment.status = PaymentStatus.REFUNDED
        payment.save()

        return ticket

    def _apply_coupon(self, coupon_code, amount, user):
        """Apply coupon with optimistic locking"""
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

        # Calculate discount
        if coupon.discount_type == 'PERCENTAGE':
            discount = amount * (coupon.discount_value / 100)
            if coupon.max_discount:
                discount = min(discount, coupon.max_discount)
        else:
            discount = coupon.discount_value

        # Update usage with atomic increment
        # Interview Note: F() expressions are atomic
        updated = Coupon.objects.filter(
            code=coupon_code,
            is_active=True
        ).update(current_usage=F('current_usage') + 1)

        if not updated:
            raise ValueError("Coupon usage limit reached")

        return discount

    @staticmethod
    def get_available_seats(show_id):
        """Get available seats - no locking for reads"""
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
            locked_by=None,
            version=F('version') + 1
        )

        return count


"""
INTERVIEW COMPARISON: Pessimistic vs Optimistic

Scenario 1: High Contention (e.g., popular movie, limited seats)
- Pessimistic: Better (less retries, guaranteed success)
- Optimistic: Many retries, wasted work

Scenario 2: Low Contention (e.g., regular movie, many seats)
- Pessimistic: Unnecessary locking overhead
- Optimistic: Better (higher concurrency, rare conflicts)

Scenario 3: Read-Heavy Operations
- Pessimistic: Can block readers
- Optimistic: Better (no blocking)

Scenario 4: Long Transactions
- Pessimistic: Holds locks longer, blocks others
- Optimistic: Better (no locks held)

Real-world BookMyShow:
- Probably uses hybrid approach
- Pessimistic for final booking
- Optimistic for seat selection/browsing
- Distributed locks (Redis) for scale
"""
