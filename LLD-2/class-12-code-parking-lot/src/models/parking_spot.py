from dataclasses import dataclass
from ..enums import SpotType, SpotStatus


@dataclass
class ParkingSpot:
    id: str
    spot_number: int
    spot_type: SpotType
    status: SpotStatus = SpotStatus.FREE
    floor_id: str = None

    def is_available(self) -> bool:
        return self.status == SpotStatus.FREE

    def occupy(self):
        self.status = SpotStatus.OCCUPIED

    def free(self):
        self.status = SpotStatus.FREE
