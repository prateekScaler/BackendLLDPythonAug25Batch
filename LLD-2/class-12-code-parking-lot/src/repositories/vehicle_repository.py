from typing import Optional
from ..models import Vehicle


class VehicleRepository:
    """In-memory repository for vehicles"""

    def __init__(self):
        self._vehicles = {}  # {license_plate: Vehicle}

    def save(self, vehicle: Vehicle) -> Vehicle:
        """Save or update a vehicle"""
        self._vehicles[vehicle.license_plate] = vehicle
        return vehicle

    def find_by_license_plate(self, license_plate: str) -> Optional[Vehicle]:
        """Find vehicle by license plate"""
        return self._vehicles.get(license_plate)
