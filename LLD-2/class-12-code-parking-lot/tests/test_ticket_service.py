import unittest
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services import TicketService
from src.repositories import ParkingSpotRepository, VehicleRepository, TicketRepository
from src.strategies import NearestSpotStrategy
from src.models import ParkingSpot, ParkingGate
from src.enums import VehicleType, SpotType, SpotStatus, GateType
from src.exceptions import NoSpotAvailableException, TicketNotFoundException


class TestTicketService(unittest.TestCase):
    """Test cases for TicketService - interview-friendly tests"""

    def setUp(self):
        """Set up test dependencies"""
        self.spot_repo = ParkingSpotRepository()
        self.vehicle_repo = VehicleRepository()
        self.ticket_repo = TicketRepository()
        self.allocation_strategy = NearestSpotStrategy()

        self.ticket_service = TicketService(
            self.spot_repo,
            self.vehicle_repo,
            self.ticket_repo,
            self.allocation_strategy
        )

        # Create test spots
        self.spot1 = ParkingSpot(
            id="SPOT-1",
            spot_number=1,
            spot_type=SpotType.MEDIUM,
            status=SpotStatus.FREE
        )
        self.spot_repo.save(self.spot1)

        # Create entry gate
        self.entry_gate = ParkingGate(gate_id="GATE-1", gate_type=GateType.ENTRY)

    def test_issue_ticket_success(self):
        """Test: Successfully issue a ticket for a car"""
        ticket = self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.vehicle.license_plate, "KA01AB1234")
        self.assertEqual(ticket.parking_spot.id, "SPOT-1")
        self.assertEqual(ticket.parking_spot.status, SpotStatus.OCCUPIED)

    def test_issue_ticket_no_spot_available(self):
        """Test: Raise exception when no spot is available"""
        # First ticket occupies the spot
        self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        # Second ticket should fail
        with self.assertRaises(NoSpotAvailableException):
            self.ticket_service.issue_ticket(
                license_plate="KA02CD5678",
                vehicle_type=VehicleType.CAR,
                entry_gate=self.entry_gate
            )

    def test_get_ticket_success(self):
        """Test: Successfully retrieve a ticket"""
        ticket = self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        retrieved_ticket = self.ticket_service.get_ticket(ticket.ticket_id)
        self.assertEqual(retrieved_ticket.ticket_id, ticket.ticket_id)

    def test_get_ticket_not_found(self):
        """Test: Raise exception when ticket not found"""
        with self.assertRaises(TicketNotFoundException):
            self.ticket_service.get_ticket("INVALID-TICKET-ID")

    def test_free_spot(self):
        """Test: Successfully free a parking spot"""
        ticket = self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        # Spot should be occupied
        self.assertEqual(ticket.parking_spot.status, SpotStatus.OCCUPIED)

        # Free the spot
        self.ticket_service.free_spot(ticket.ticket_id)

        # Spot should be free now
        self.assertEqual(ticket.parking_spot.status, SpotStatus.FREE)


if __name__ == '__main__':
    unittest.main()
