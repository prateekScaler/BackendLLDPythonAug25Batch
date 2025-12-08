from datetime import datetime
from typing import Optional
import uuid

from ..models import ParkingTicket, Vehicle, ParkingGate, ParkingAttendant
from ..enums import VehicleType, SpotStatus
from ..repositories import ParkingSpotRepository, VehicleRepository, TicketRepository
from ..strategies import SpotAllocationStrategy
from ..exceptions import NoSpotAvailableException, TicketNotFoundException


class TicketService:
    """Service for handling parking ticket operations"""

    def __init__(
        self,
        spot_repository: ParkingSpotRepository,
        vehicle_repository: VehicleRepository,
        ticket_repository: TicketRepository,
        allocation_strategy: SpotAllocationStrategy
    ):
        self.spot_repository = spot_repository
        self.vehicle_repository = vehicle_repository
        self.ticket_repository = ticket_repository
        self.allocation_strategy = allocation_strategy

    def issue_ticket(
        self,
        license_plate: str,
        vehicle_type: VehicleType,
        entry_gate: ParkingGate,
        entry_operator: Optional[ParkingAttendant] = None
    ) -> ParkingTicket:
        """Issue a new parking ticket"""

        # Find or create vehicle
        vehicle = self.vehicle_repository.find_by_license_plate(license_plate)
        if not vehicle:
            vehicle = Vehicle(license_plate=license_plate, vehicle_type=vehicle_type)
            self.vehicle_repository.save(vehicle)

        # Find available spot using allocation strategy
        available_spots = self.spot_repository.find_available()
        spot = self.allocation_strategy.find_spot(available_spots, vehicle_type)

        if not spot:
            raise NoSpotAvailableException(vehicle_type)

        # Occupy the spot
        spot.occupy()
        self.spot_repository.save(spot)

        # Create ticket
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        ticket = ParkingTicket(
            ticket_id=ticket_id,
            vehicle=vehicle,
            parking_spot=spot,
            entry_gate=entry_gate,
            entry_time=datetime.now(),
            entry_operator=entry_operator
        )

        self.ticket_repository.save(ticket)
        return ticket

    def get_ticket(self, ticket_id: str) -> ParkingTicket:
        """Get ticket by ID"""
        ticket = self.ticket_repository.find_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundException(ticket_id)
        return ticket

    def free_spot(self, ticket_id: str):
        """Free the parking spot associated with a ticket"""
        ticket = self.get_ticket(ticket_id)
        ticket.parking_spot.free()
        self.spot_repository.save(ticket.parking_spot)
