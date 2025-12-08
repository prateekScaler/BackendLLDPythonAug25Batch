from typing import Optional, List
from ..models import Payment


class PaymentRepository:
    """In-memory repository for payments"""

    def __init__(self):
        self._payments = {}  # {payment_id: Payment}
        self._ticket_payment_map = {}  # {ticket_id: payment_id}

    def save(self, payment: Payment) -> Payment:
        """Save or update a payment"""
        self._payments[payment.payment_id] = payment
        self._ticket_payment_map[payment.ticket_id] = payment.payment_id
        return payment

    def find_by_id(self, payment_id: str) -> Optional[Payment]:
        """Find payment by ID"""
        return self._payments.get(payment_id)

    def find_by_ticket_id(self, ticket_id: str) -> Optional[Payment]:
        """Find payment by ticket ID"""
        payment_id = self._ticket_payment_map.get(ticket_id)
        if payment_id:
            return self._payments.get(payment_id)
        return None

    def find_all(self) -> List[Payment]:
        """Get all payments"""
        return list(self._payments.values())
