"""
Booking Service - Pessimistic Locking Implementation

CONCURRENCY CONTROL: Database-level pessimistic locking using SELECT FOR UPDATE

Interview Points:
1. Uses database row-level locks
2. Prevents race conditions at DB level
3. Transaction holds lock until commit/rollback
4. Other transactions wait (blocking)
5. Best for high-contention scenarios

Pros:
- Guaranteed consistency
- No need for retry logic
- Simple to implement

Cons:
- Can cause deadlocks
- Reduced concurrency (blocking)
- Potential performance bottleneck

When to use:
- High probability of conflicts
- Critical operations (payment, inventory)
- When retry logic is not acceptable
"""
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import uuid

from ..models import (
    Show, ShowSeat, Ticket, TicketSeat, Payment,
    SeatStatus, TicketStatus, PaymentStatus, Coupon
)
from .base_service import BaseService


class BookingServicePessimistic(BaseService):
    """
    Booking service using pessimistic (database) locking
    Interview Note: select_for_update() acquires row-level lock
    """

    @transaction.atomic  # Critical: Ensures atomicity
    def book_tickets(self, user, show_id, seat_ids, payment_mode, coupon_code=None):
        """
        Book tickets with pessimistic locking

        Flow:
        1. Lock the show seats (SELECT FOR UPDATE)
        2. Validate availability
        3. Lock seats temporarily
        4. Create ticket and payment
        5. Commit transaction (releases lock)

        Interview Question: What happens if two users try to book same seats?
        Answer: Second transaction waits until first completes, then fails validation
        """

        # Step 1: Lock and fetch show seats
        # select_for_update() acquires exclusive row lock
        # nowait=False means wait for lock (can use nowait=True to fail immediately)
        show_seats = list(
            ShowSeat.objects.select_for_update()
            .filter(
                show_id=show_id,
                id__in=seat_ids
            )
            .select_related('seat', 'show', 'show__movie')
        )

        if len(show_seats) != len(seat_ids):
            raise ValueError("Some seats not found")

        # Step 2: Validate all seats are available
        # This check is safe because we hold the lock
        unavailable_seats = [
            ss.seat.number for ss in show_seats
            if ss.status != SeatStatus.AVAILABLE
        ]

        if unavailable_seats:
            raise ValueError(
                f"Seats not available: {', '.join(unavailable_seats)}"
            )

        # Step 3: Validate booking time
        show = show_seats[0].show
        if not show.is_booking_allowed():
            raise ValueError("Booking cutoff time has passed")

        # Step 4: Calculate total amount
        total_amount = sum(ss.price for ss in show_seats)

        # Step 5: Apply coupon if provided
        discount = 0
        if coupon_code:
            discount = self._apply_coupon(coupon_code, total_amount, user)
            total_amount -= discount

        # Step 6: Lock seats temporarily (update status)
        ShowSeat.objects.filter(
            id__in=[ss.id for ss in show_seats]
        ).update(
            status=SeatStatus.LOCKED,
            locked_at=timezone.now(),
            locked_by=user
        )

        # Step 7: Create ticket
        ticket = Ticket.objects.create(
            id=f"TKT-{uuid.uuid4().hex[:12].upper()}",
            user=user,
            show=show,
            amount=total_amount,
            status=TicketStatus.BOOKED
        )

        # Step 8: Create ticket-seat associations
        ticket_seats = [
            TicketSeat(ticket=ticket, show_seat=ss)
            for ss in show_seats
        ]
        TicketSeat.objects.bulk_create(ticket_seats)

        # Step 9: Create payment record
        payment = Payment.objects.create(
            id=f"PAY-{uuid.uuid4().hex[:12].upper()}",
            ticket=ticket,
            amount=total_amount,
            mode=payment_mode,
            status=PaymentStatus.PENDING,
            transaction_id=f"TXN-{uuid.uuid4().hex[:16].upper()}"
        )

        # Transaction commits here, locks are released
        # If any exception occurs, entire transaction rolls back

        return {
            'ticket': ticket,
            'payment': payment,
            'total_amount': total_amount,
            'discount': discount
        }

    @transaction.atomic
    def confirm_booking(self, ticket_id, payment_success=True):
        """
        Confirm booking after payment

        Interview Note: Separate transaction for payment confirmation
        """
        ticket = Ticket.objects.select_for_update().get(id=ticket_id)
        payment = ticket.payment

        if payment_success:
            # Mark seats as booked
            ShowSeat.objects.filter(
                ticket_seats__ticket=ticket
            ).update(status=SeatStatus.BOOKED)

            # Update ticket status
            ticket.status = TicketStatus.CONFIRMED
            ticket.save()

            # Update payment status
            payment.status = PaymentStatus.SUCCESS
            payment.save()
        else:
            # Release seats
            ShowSeat.objects.filter(
                ticket_seats__ticket=ticket
            ).update(
                status=SeatStatus.AVAILABLE,
                locked_at=None,
                locked_by=None
            )

            # Cancel ticket
            ticket.status = TicketStatus.CANCELLED
            ticket.save()

            # Mark payment as failed
            payment.status = PaymentStatus.FAILED
            payment.save()

        return ticket

    @transaction.atomic
    def cancel_booking(self, ticket_id, user):
        """
        Cancel booking and refund

        Interview Points:
        1. Validate cancellation eligibility
        2. Release seats atomically
        3. Process refund
        """
        ticket = Ticket.objects.select_for_update().select_related(
            'show', 'payment'
        ).get(id=ticket_id)

        # Validate ownership
        if ticket.user != user:
            raise PermissionError("Not authorized to cancel this ticket")

        # Validate cancellation window
        if not ticket.can_cancel():
            raise ValueError("Cannot cancel: cutoff time passed or already cancelled")

        # Release seats
        ShowSeat.objects.filter(
            ticket_seats__ticket=ticket
        ).update(
            status=SeatStatus.AVAILABLE,
            locked_at=None,
            locked_by=None
        )

        # Update ticket
        ticket.status = TicketStatus.CANCELLED
        ticket.save()

        # Process refund
        payment = ticket.payment
        payment.status = PaymentStatus.REFUNDED
        payment.save()

        return ticket

    def _apply_coupon(self, coupon_code, amount, user):
        """
        Apply coupon and calculate discount

        Interview Note: Separate method for single responsibility
        """
        try:
            coupon = Coupon.objects.select_for_update().get(code=coupon_code)
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
        else:  # FIXED
            discount = coupon.discount_value

        # Update coupon usage
        coupon.current_usage += 1
        coupon.save()

        return discount

    @staticmethod
    def get_available_seats(show_id):
        """
        Get available seats for a show

        Interview Note: No locking needed for read operations
        Use select_related to optimize queries
        """
        return ShowSeat.objects.filter(
            show_id=show_id,
            status=SeatStatus.AVAILABLE
        ).select_related('seat').order_by('seat__number')

    @staticmethod
    def cleanup_expired_locks():
        """
        Cleanup seats locked for too long (e.g., payment timeout)

        Interview Note: Background job to handle abandoned locks
        Run this periodically (cron job/celery task)
        """
        timeout = timezone.now() - timedelta(minutes=10)

        expired_locks = ShowSeat.objects.filter(
            status=SeatStatus.LOCKED,
            locked_at__lt=timeout
        )

        count = expired_locks.update(
            status=SeatStatus.AVAILABLE,
            locked_at=None,
            locked_by=None
        )

        return count
