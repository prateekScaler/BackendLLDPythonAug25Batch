import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.controllers import TicketController, PaymentController
from src.services import TicketService, PaymentService
from src.repositories import (
    ParkingSpotRepository,
    VehicleRepository,
    TicketRepository,
    PaymentRepository
)
from src.strategies import NearestSpotStrategy, HourlyPricingStrategy
from src.models import ParkingSpot
from src.enums import SpotType, SpotStatus


class TestTicketController(unittest.TestCase):
    """Test cases for TicketController"""

    def setUp(self):
        """Set up test dependencies"""
        spot_repo = ParkingSpotRepository()
        vehicle_repo = VehicleRepository()
        ticket_repo = TicketRepository()
        allocation_strategy = NearestSpotStrategy()

        ticket_service = TicketService(
            spot_repo, vehicle_repo, ticket_repo, allocation_strategy
        )

        self.controller = TicketController(ticket_service)

        # Add test spot
        spot = ParkingSpot(id="SPOT-1", spot_number=1, spot_type=SpotType.MEDIUM)
        spot_repo.save(spot)

    def test_issue_ticket_success(self):
        """Test: Successfully issue ticket via controller"""
        request_data = {
            'license_plate': 'KA01AB1234',
            'vehicle_type': 'CAR',
            'entry_gate_id': 'GATE-1'
        }

        response, status_code = self.controller.issue_ticket(request_data)

        self.assertEqual(status_code, 201)
        self.assertEqual(response['status'], 'success')
        self.assertIn('ticket_id', response['data'])
        self.assertEqual(response['data']['vehicle']['license_plate'], 'KA01AB1234')

    def test_issue_ticket_missing_license_plate(self):
        """Test: Return 400 when license_plate is missing"""
        request_data = {
            'vehicle_type': 'CAR'
        }

        response, status_code = self.controller.issue_ticket(request_data)

        self.assertEqual(status_code, 400)
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['error']['code'], 'VALIDATION_ERROR')

    def test_issue_ticket_invalid_vehicle_type(self):
        """Test: Return 400 for invalid vehicle type"""
        request_data = {
            'license_plate': 'KA01AB1234',
            'vehicle_type': 'SPACESHIP'
        }

        response, status_code = self.controller.issue_ticket(request_data)

        self.assertEqual(status_code, 400)
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['error']['code'], 'INVALID_VEHICLE_TYPE')

    def test_get_ticket_success(self):
        """Test: Successfully get ticket details"""
        # First issue a ticket
        request_data = {
            'license_plate': 'KA01AB1234',
            'vehicle_type': 'CAR'
        }
        issue_response, _ = self.controller.issue_ticket(request_data)
        ticket_id = issue_response['data']['ticket_id']

        # Now get the ticket
        response, status_code = self.controller.get_ticket(ticket_id)

        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['data']['ticket_id'], ticket_id)

    def test_get_ticket_not_found(self):
        """Test: Return 404 for non-existent ticket"""
        response, status_code = self.controller.get_ticket('INVALID-ID')

        self.assertEqual(status_code, 404)
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['error']['code'], 'TICKET_NOT_FOUND')


class TestPaymentController(unittest.TestCase):
    """Test cases for PaymentController"""

    def setUp(self):
        """Set up test dependencies"""
        self.spot_repo = ParkingSpotRepository()
        vehicle_repo = VehicleRepository()
        ticket_repo = TicketRepository()
        payment_repo = PaymentRepository()

        allocation_strategy = NearestSpotStrategy()
        pricing_strategy = HourlyPricingStrategy()

        self.ticket_service = TicketService(
            self.spot_repo, vehicle_repo, ticket_repo, allocation_strategy
        )
        payment_service = PaymentService(
            payment_repo, ticket_repo, pricing_strategy
        )

        self.ticket_controller = TicketController(self.ticket_service)
        self.payment_controller = PaymentController(payment_service)

        # Add test spot
        spot = ParkingSpot(id="SPOT-1", spot_number=1, spot_type=SpotType.MEDIUM)
        self.spot_repo.save(spot)

    def test_process_payment_success(self):
        """Test: Successfully process payment"""
        # Issue ticket first
        ticket_response, _ = self.ticket_controller.issue_ticket({
            'license_plate': 'KA01AB1234',
            'vehicle_type': 'CAR'
        })
        ticket_id = ticket_response['data']['ticket_id']

        # Process payment
        payment_request = {
            'ticket_id': ticket_id,
            'payment_type': 'UPI'
        }
        response, status_code = self.payment_controller.process_payment(payment_request)

        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], 'success')
        self.assertIn('payment_id', response['data'])
        self.assertEqual(response['data']['payment_type'], 'UPI')
        self.assertEqual(response['data']['status'], 'DONE')

    def test_process_payment_missing_ticket_id(self):
        """Test: Return 400 when ticket_id is missing"""
        request_data = {
            'payment_type': 'CASH'
        }

        response, status_code = self.payment_controller.process_payment(request_data)

        self.assertEqual(status_code, 400)
        self.assertEqual(response['error']['code'], 'VALIDATION_ERROR')

    def test_process_payment_invalid_payment_type(self):
        """Test: Return 400 for invalid payment type"""
        request_data = {
            'ticket_id': 'TKT-123',
            'payment_type': 'BITCOIN'
        }

        response, status_code = self.payment_controller.process_payment(request_data)

        self.assertEqual(status_code, 400)
        self.assertEqual(response['error']['code'], 'INVALID_PAYMENT_TYPE')

    def test_checkout_success(self):
        """Test: Successfully checkout with invoice"""
        # Issue ticket
        ticket_response, _ = self.ticket_controller.issue_ticket({
            'license_plate': 'KA01AB1234',
            'vehicle_type': 'CAR'
        })
        ticket_id = ticket_response['data']['ticket_id']

        # Process payment
        self.payment_controller.process_payment({
            'ticket_id': ticket_id,
            'payment_type': 'CASH'
        })

        # Checkout
        checkout_request = {
            'ticket_id': ticket_id,
            'exit_gate_id': 'GATE-2'
        }
        response, status_code = self.payment_controller.checkout(checkout_request)

        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], 'success')
        self.assertIn('invoice_id', response['data'])
        self.assertEqual(response['data']['ticket_id'], ticket_id)

    def test_checkout_without_payment(self):
        """Test: Return 400 when checkout without payment"""
        # Issue ticket but don't pay
        ticket_response, _ = self.ticket_controller.issue_ticket({
            'license_plate': 'KA01AB1234',
            'vehicle_type': 'CAR'
        })
        ticket_id = ticket_response['data']['ticket_id']

        # Try to checkout without paying
        checkout_request = {
            'ticket_id': ticket_id
        }
        response, status_code = self.payment_controller.checkout(checkout_request)

        self.assertEqual(status_code, 400)
        self.assertEqual(response['error']['code'], 'PAYMENT_NOT_DONE')


if __name__ == '__main__':
    unittest.main()
