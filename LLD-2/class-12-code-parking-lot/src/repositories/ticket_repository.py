from typing import Optional, List
from ..models import ParkingTicket


class TicketRepository:
    """In-memory repository for parking tickets"""

    def __init__(self):
        self._tickets = {}  # {ticket_id: ParkingTicket}

    def save(self, ticket: ParkingTicket) -> ParkingTicket:
        """Save or update a ticket"""
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def find_by_id(self, ticket_id: str) -> Optional[ParkingTicket]:
        """Find ticket by ID"""
        return self._tickets.get(ticket_id)

    def find_all(self) -> List[ParkingTicket]:
        """Get all tickets"""
        return list(self._tickets.values())
