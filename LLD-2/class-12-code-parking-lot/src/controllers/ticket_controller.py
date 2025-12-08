"""
Ticket Controller - Handles HTTP requests for ticket operations

This is the Presentation Layer that sits above the Service Layer.
Controllers are responsible for:
1. Request validation
2. Calling service methods
3. Formatting responses
4. HTTP status codes
5. Error handling and formatting
"""

from typing import Dict, Any
from ..services import TicketService
from ..enums import VehicleType
from ..exceptions import NoSpotAvailableException, TicketNotFoundException


class TicketController:
    """Controller for ticket-related API endpoints"""

    def __init__(self, ticket_service: TicketService):
        self.ticket_service = ticket_service

    def issue_ticket(self, request_data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        """
        POST /tickets
        Issue a new parking ticket

        Request body:
        {
            "license_plate": "KA01AB1234",
            "vehicle_type": "CAR",
            "entry_gate_id": "GATE-1"
        }

        Returns: (response_dict, status_code)
        """
        try:
            # Validate request
            license_plate = request_data.get('license_plate')
            vehicle_type_str = request_data.get('vehicle_type')
            entry_gate_id = request_data.get('entry_gate_id')

            if not license_plate:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'license_plate is required'
                    }
                }, 400

            if not vehicle_type_str:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'vehicle_type is required'
                    }
                }, 400

            # Convert string to enum
            try:
                vehicle_type = VehicleType[vehicle_type_str.upper()]
            except KeyError:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'INVALID_VEHICLE_TYPE',
                        'message': f'Invalid vehicle type: {vehicle_type_str}'
                    }
                }, 400

            # For simplicity, we'll create a mock gate
            # In real implementation, you'd fetch this from repository
            from ..models import ParkingGate
            from ..enums import GateType
            entry_gate = ParkingGate(gate_id=entry_gate_id or "GATE-1", gate_type=GateType.ENTRY)

            # Call service
            ticket = self.ticket_service.issue_ticket(
                license_plate=license_plate,
                vehicle_type=vehicle_type,
                entry_gate=entry_gate
            )

            # Format response
            return {
                'status': 'success',
                'data': {
                    'ticket_id': ticket.ticket_id,
                    'entry_time': ticket.entry_time.isoformat(),
                    'parking_spot': {
                        'spot_id': ticket.parking_spot.id,
                        'spot_number': ticket.parking_spot.spot_number,
                        'spot_type': ticket.parking_spot.spot_type.value,
                        'floor_id': ticket.parking_spot.floor_id
                    },
                    'vehicle': {
                        'license_plate': ticket.vehicle.license_plate,
                        'vehicle_type': ticket.vehicle.vehicle_type.value
                    }
                }
            }, 201  # 201 Created

        except NoSpotAvailableException as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'NO_SPOT_AVAILABLE',
                    'message': str(e)
                }
            }, 404

        except Exception as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'An unexpected error occurred'
                }
            }, 500

    def get_ticket(self, ticket_id: str) -> tuple[Dict[str, Any], int]:
        """
        GET /tickets/{ticket_id}
        Get ticket details

        Returns: (response_dict, status_code)
        """
        try:
            ticket = self.ticket_service.get_ticket(ticket_id)

            return {
                'status': 'success',
                'data': {
                    'ticket_id': ticket.ticket_id,
                    'entry_time': ticket.entry_time.isoformat(),
                    'parking_spot': {
                        'spot_id': ticket.parking_spot.id,
                        'spot_number': ticket.parking_spot.spot_number,
                        'spot_type': ticket.parking_spot.spot_type.value,
                        'status': ticket.parking_spot.status.value
                    },
                    'vehicle': {
                        'license_plate': ticket.vehicle.license_plate,
                        'vehicle_type': ticket.vehicle.vehicle_type.value
                    }
                }
            }, 200

        except TicketNotFoundException as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'TICKET_NOT_FOUND',
                    'message': str(e)
                }
            }, 404

        except Exception as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'An unexpected error occurred'
                }
            }, 500
