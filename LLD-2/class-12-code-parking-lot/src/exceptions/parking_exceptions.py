class ParkingLotException(Exception):
    """Base exception for parking lot system"""
    pass


class NoSpotAvailableException(ParkingLotException):
    """Raised when no parking spot is available for the vehicle type"""
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type
        super().__init__(f"No spot available for vehicle type: {vehicle_type}")


class TicketNotFoundException(ParkingLotException):
    """Raised when ticket is not found"""
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        super().__init__(f"Ticket not found: {ticket_id}")


class PaymentNotFoundException(ParkingLotException):
    """Raised when payment is not found"""
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        super().__init__(f"Payment not found for ticket: {ticket_id}")


class PaymentAlreadyDoneException(ParkingLotException):
    """Raised when trying to pay for already paid ticket"""
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        super().__init__(f"Payment already done for ticket: {ticket_id}")


class InvalidVehicleTypeException(ParkingLotException):
    """Raised when vehicle type is invalid"""
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type
        super().__init__(f"Invalid vehicle type: {vehicle_type}")


class SpotAlreadyOccupiedException(ParkingLotException):
    """Raised when trying to assign an occupied spot"""
    def __init__(self, spot_id):
        self.spot_id = spot_id
        super().__init__(f"Spot already occupied: {spot_id}")
