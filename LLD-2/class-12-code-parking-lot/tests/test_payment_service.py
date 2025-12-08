import unittest
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services import PaymentService, TicketService
from src.repositories import (
    PaymentRepository,
    TicketRepository,
    ParkingSpotRepository,
    VehicleRepository
)
from src.strategies import HourlyPricingStrategy, NearestSpotStrategy
from src.models import ParkingSpot, ParkingGate
from src.enums import VehicleType, SpotType, SpotStatus, GateType, PaymentType, PaymentStatus
from src.exceptions import PaymentAlreadyDoneException, TicketNotFoundException


class TestPaymentService(unittest.TestCase):
    """Test cases for PaymentService - interview-friendly tests"""

    def setUp(self):
        """Set up test dependencies"""
        self.payment_repo = PaymentRepository()
        self.ticket_repo = TicketRepository()
        self.spot_repo = ParkingSpotRepository()
        self.vehicle_repo = VehicleRepository()

        self.pricing_strategy = HourlyPricingStrategy()
        self.allocation_strategy = NearestSpotStrategy()

        self.payment_service = PaymentService(
            self.payment_repo,
            self.ticket_repo,
            self.pricing_strategy
        )

        self.ticket_service = TicketService(
            self.spot_repo,
            self.vehicle_repo,
            self.ticket_repo,
            self.allocation_strategy
        )

        # Create test spot
        spot = ParkingSpot(
            id="SPOT-1",
            spot_number=1,
            spot_type=SpotType.MEDIUM,
            status=SpotStatus.FREE
        )
        self.spot_repo.save(spot)

        # Create entry gate
        self.entry_gate = ParkingGate(gate_id="GATE-1", gate_type=GateType.ENTRY)

    def test_process_payment_success(self):
        """Test: Successfully process a payment"""
        # Issue ticket
        ticket = self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        # Process payment
        payment = self.payment_service.process_payment(
            ticket.ticket_id,
            PaymentType.CASH
        )

        self.assertIsNotNone(payment)
        self.assertEqual(payment.ticket_id, ticket.ticket_id)
        self.assertEqual(payment.status, PaymentStatus.DONE)
        self.assertGreater(payment.amount, 0)

    def test_process_payment_calculates_correct_amount(self):
        """Test: Payment calculates correct amount for 1 hour"""
        ticket = self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        payment = self.payment_service.process_payment(
            ticket.ticket_id,
            PaymentType.UPI
        )

        # For MEDIUM spot, first hour should be 80
        self.assertEqual(payment.amount, 80)

    def test_process_payment_already_paid(self):
        """Test: Raise exception when payment already done"""
        ticket = self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        # First payment
        self.payment_service.process_payment(
            ticket.ticket_id,
            PaymentType.CASH
        )

        # Second payment should fail
        with self.assertRaises(PaymentAlreadyDoneException):
            self.payment_service.process_payment(
                ticket.ticket_id,
                PaymentType.CASH
            )

    def test_process_payment_invalid_ticket(self):
        """Test: Raise exception for invalid ticket"""
        with self.assertRaises(TicketNotFoundException):
            self.payment_service.process_payment(
                "INVALID-TICKET",
                PaymentType.CASH
            )

    def test_generate_invoice(self):
        """Test: Successfully generate invoice"""
        ticket = self.ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=self.entry_gate
        )

        payment = self.payment_service.process_payment(
            ticket.ticket_id,
            PaymentType.CASH
        )

        invoice = self.payment_service.generate_invoice(ticket.ticket_id)

        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.ticket.ticket_id, ticket.ticket_id)
        self.assertEqual(invoice.amount, payment.amount)


if __name__ == '__main__':
    unittest.main()
