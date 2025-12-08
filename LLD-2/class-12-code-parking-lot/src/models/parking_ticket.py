from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .vehicle import Vehicle
from .parking_spot import ParkingSpot
from .parking_gate import ParkingGate
from .parking_attendant import ParkingAttendant


@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle: Vehicle
    parking_spot: ParkingSpot
    entry_gate: ParkingGate
    entry_time: datetime
    entry_operator: Optional[ParkingAttendant] = None
