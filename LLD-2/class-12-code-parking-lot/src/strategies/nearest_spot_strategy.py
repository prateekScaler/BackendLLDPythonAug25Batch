from typing import Optional, List
from .spot_allocation_strategy import SpotAllocationStrategy
from ..models import ParkingSpot
from ..enums import VehicleType, SpotType


class NearestSpotStrategy(SpotAllocationStrategy):
    """Allocates the first available spot (nearest to entry)"""

    # Mapping vehicle type to required spot type
    VEHICLE_TO_SPOT_MAPPING = {
        VehicleType.BIKE: SpotType.SMALL,
        VehicleType.SCOOTER: SpotType.SMALL,
        VehicleType.CAR: SpotType.MEDIUM,
        VehicleType.TRUCK: SpotType.LARGE,
        VehicleType.BUS: SpotType.LARGE,
    }

    def find_spot(self, available_spots: List[ParkingSpot], vehicle_type: VehicleType) -> Optional[ParkingSpot]:
        """Find the first available spot matching the vehicle type"""
        required_spot_type = self.VEHICLE_TO_SPOT_MAPPING.get(vehicle_type)

        if not required_spot_type:
            return None

        for spot in available_spots:
            if spot.spot_type == required_spot_type and spot.is_available():
                return spot

        return None
