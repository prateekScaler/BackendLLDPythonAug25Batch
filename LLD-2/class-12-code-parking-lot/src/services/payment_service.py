from datetime import datetime
import uuid

from ..models import Payment, Invoice
from ..enums import PaymentType, PaymentStatus
from ..repositories import PaymentRepository, TicketRepository
from ..strategies import PricingStrategy
from ..exceptions import (
    TicketNotFoundException,
    PaymentAlreadyDoneException,
    PaymentNotFoundException
)


class PaymentService:
    """Service for handling payment operations"""

    def __init__(
        self,
        payment_repository: PaymentRepository,
        ticket_repository: TicketRepository,
        pricing_strategy: PricingStrategy
    ):
        self.payment_repository = payment_repository
        self.ticket_repository = ticket_repository
        self.pricing_strategy = pricing_strategy

    def process_payment(
        self,
        ticket_id: str,
        payment_type: PaymentType
    ) -> Payment:
        """Process payment for a parking ticket"""

        # Get ticket
        ticket = self.ticket_repository.find_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundException(ticket_id)

        # Check if payment already exists
        existing_payment = self.payment_repository.find_by_ticket_id(ticket_id)
        if existing_payment and existing_payment.status == PaymentStatus.DONE:
            raise PaymentAlreadyDoneException(ticket_id)

        # Calculate amount
        current_time = datetime.now()
        amount = self.pricing_strategy.calculate_fee(
            ticket.entry_time,
            current_time,
            ticket.parking_spot.spot_type
        )

        # Create payment
        payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        payment = Payment(
            payment_id=payment_id,
            ticket_id=ticket_id,
            amount=amount,
            payment_type=payment_type,
            status=PaymentStatus.DONE,
            payment_time=current_time
        )

        self.payment_repository.save(payment)
        return payment

    def get_payment(self, ticket_id: str) -> Payment:
        """Get payment for a ticket"""
        payment = self.payment_repository.find_by_ticket_id(ticket_id)
        if not payment:
            raise PaymentNotFoundException(ticket_id)
        return payment

    def generate_invoice(self, ticket_id: str) -> Invoice:
        """Generate invoice for a ticket"""
        ticket = self.ticket_repository.find_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundException(ticket_id)

        payment = self.get_payment(ticket_id)

        invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
        invoice = Invoice(
            invoice_id=invoice_id,
            ticket=ticket,
            exit_time=datetime.now(),
            amount=payment.amount,
            payment=payment
        )

        return invoice
