from dataclasses import dataclass, field
from typing import List
from .parking_spot import ParkingSpot


@dataclass
class ParkingFloor:
    id: str
    floor_number: int
    parking_spots: List[ParkingSpot] = field(default_factory=list)

    def add_spot(self, spot: ParkingSpot):
        spot.floor_id = self.id
        self.parking_spots.append(spot)

    def get_available_spots(self):
        return [spot for spot in self.parking_spots if spot.is_available()]
