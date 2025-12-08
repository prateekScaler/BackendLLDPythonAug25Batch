from dataclasses import dataclass, field
from typing import List
from .parking_floor import ParkingFloor
from .parking_gate import ParkingGate


@dataclass
class ParkingLot:
    id: str
    name: str
    address: str
    parking_floors: List[ParkingFloor] = field(default_factory=list)
    entry_gates: List[ParkingGate] = field(default_factory=list)
    exit_gates: List[ParkingGate] = field(default_factory=list)

    def add_floor(self, floor: ParkingFloor):
        self.parking_floors.append(floor)

    def add_entry_gate(self, gate: ParkingGate):
        self.entry_gates.append(gate)

    def add_exit_gate(self, gate: ParkingGate):
        self.exit_gates.append(gate)
