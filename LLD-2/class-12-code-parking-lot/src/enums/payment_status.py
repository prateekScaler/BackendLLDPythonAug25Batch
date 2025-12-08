from enum import Enum


class PaymentStatus(Enum):
    PENDING = "PENDING"
    DONE = "DONE"
    FAILED = "FAILED"
