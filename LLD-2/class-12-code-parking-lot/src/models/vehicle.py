from dataclasses import dataclass
from ..enums import VehicleType


@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType

    def __post_init__(self):
        if not isinstance(self.vehicle_type, VehicleType):
            raise ValueError(f"Invalid vehicle type: {self.vehicle_type}")
