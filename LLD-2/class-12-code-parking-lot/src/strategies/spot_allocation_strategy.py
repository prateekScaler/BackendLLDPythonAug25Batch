from abc import ABC, abstractmethod
from typing import Optional, List
from ..models import ParkingSpot
from ..enums import VehicleType


class SpotAllocationStrategy(ABC):
    """Abstract base class for spot allocation strategies"""

    @abstractmethod
    def find_spot(self, available_spots: List[ParkingSpot], vehicle_type: VehicleType) -> Optional[ParkingSpot]:
        """Find a suitable parking spot for the given vehicle type"""
        pass
