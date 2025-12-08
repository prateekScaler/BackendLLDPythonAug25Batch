import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.strategies import NearestSpotStrategy
from src.models import ParkingSpot
from src.enums import VehicleType, SpotType, SpotStatus


class TestSpotAllocation(unittest.TestCase):
    """Test cases for spot allocation strategies - interview-friendly tests"""

    def setUp(self):
        """Set up test data"""
        self.strategy = NearestSpotStrategy()

        self.small_spot = ParkingSpot(
            id="SPOT-1",
            spot_number=1,
            spot_type=SpotType.SMALL,
            status=SpotStatus.FREE
        )

        self.medium_spot = ParkingSpot(
            id="SPOT-2",
            spot_number=2,
            spot_type=SpotType.MEDIUM,
            status=SpotStatus.FREE
        )

        self.large_spot = ParkingSpot(
            id="SPOT-3",
            spot_number=3,
            spot_type=SpotType.LARGE,
            status=SpotStatus.FREE
        )

    def test_allocate_bike_to_small_spot(self):
        """Test: Bike should be allocated to SMALL spot"""
        spots = [self.small_spot, self.medium_spot, self.large_spot]
        allocated = self.strategy.find_spot(spots, VehicleType.BIKE)

        self.assertIsNotNone(allocated)
        self.assertEqual(allocated.spot_type, SpotType.SMALL)

    def test_allocate_car_to_medium_spot(self):
        """Test: Car should be allocated to MEDIUM spot"""
        spots = [self.small_spot, self.medium_spot, self.large_spot]
        allocated = self.strategy.find_spot(spots, VehicleType.CAR)

        self.assertIsNotNone(allocated)
        self.assertEqual(allocated.spot_type, SpotType.MEDIUM)

    def test_allocate_truck_to_large_spot(self):
        """Test: Truck should be allocated to LARGE spot"""
        spots = [self.small_spot, self.medium_spot, self.large_spot]
        allocated = self.strategy.find_spot(spots, VehicleType.TRUCK)

        self.assertIsNotNone(allocated)
        self.assertEqual(allocated.spot_type, SpotType.LARGE)

    def test_no_allocation_when_no_matching_spot(self):
        """Test: Return None when no matching spot available"""
        spots = [self.small_spot]  # Only small spot available
        allocated = self.strategy.find_spot(spots, VehicleType.CAR)  # Car needs medium

        self.assertIsNone(allocated)

    def test_no_allocation_when_spot_occupied(self):
        """Test: Return None when matching spot is occupied"""
        self.medium_spot.status = SpotStatus.OCCUPIED
        spots = [self.medium_spot]
        allocated = self.strategy.find_spot(spots, VehicleType.CAR)

        self.assertIsNone(allocated)


if __name__ == '__main__':
    unittest.main()
