from dataclasses import dataclass
from typing import Optional
from ..enums import GateType
from .parking_attendant import ParkingAttendant


@dataclass
class ParkingGate:
    gate_id: str
    gate_type: GateType
    attendant: Optional[ParkingAttendant] = None
