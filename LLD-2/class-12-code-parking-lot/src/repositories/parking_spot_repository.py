from typing import List, Optional
from ..models import ParkingSpot
from ..enums import SpotStatus, SpotType


class ParkingSpotRepository:
    """In-memory repository for parking spots"""

    def __init__(self):
        self._spots = {}  # {spot_id: ParkingSpot}

    def save(self, spot: ParkingSpot) -> ParkingSpot:
        """Save or update a parking spot"""
        self._spots[spot.id] = spot
        return spot

    def find_by_id(self, spot_id: str) -> Optional[ParkingSpot]:
        """Find spot by ID"""
        return self._spots.get(spot_id)

    def find_all(self) -> List[ParkingSpot]:
        """Get all spots"""
        return list(self._spots.values())

    def find_available_by_type(self, spot_type: SpotType) -> List[ParkingSpot]:
        """Find all available spots of a specific type"""
        return [
            spot for spot in self._spots.values()
            if spot.spot_type == spot_type and spot.status == SpotStatus.FREE
        ]

    def find_available(self) -> List[ParkingSpot]:
        """Find all available spots"""
        return [
            spot for spot in self._spots.values()
            if spot.status == SpotStatus.FREE
        ]

    def update_status(self, spot_id: str, status: SpotStatus) -> Optional[ParkingSpot]:
        """Update spot status"""
        spot = self.find_by_id(spot_id)
        if spot:
            spot.status = status
        return spot
