from dataclasses import dataclass
from datetime import datetime
from ..enums import PaymentType, PaymentStatus


@dataclass
class Payment:
    payment_id: str
    ticket_id: str
    amount: float
    payment_type: PaymentType
    status: PaymentStatus
    payment_time: datetime
