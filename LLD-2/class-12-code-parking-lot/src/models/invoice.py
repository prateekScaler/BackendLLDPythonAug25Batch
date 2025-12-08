from dataclasses import dataclass
from datetime import datetime
from .parking_ticket import ParkingTicket
from .payment import Payment


@dataclass
class Invoice:
    invoice_id: str
    ticket: ParkingTicket
    exit_time: datetime
    amount: float
    payment: Payment
