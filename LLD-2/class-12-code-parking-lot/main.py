"""
Demo script showing the complete parking lot system in action
"""

from src.services import TicketService, PaymentService
from src.repositories import (
    ParkingSpotRepository,
    VehicleRepository,
    TicketRepository,
    PaymentRepository
)
from src.strategies import NearestSpotStrategy, HourlyPricingStrategy
from src.models import ParkingSpot, ParkingGate, ParkingAttendant
from src.enums import VehicleType, SpotType, SpotStatus, GateType, PaymentType


def setup_parking_lot():
    """Initialize parking lot with spots and gates"""
    spot_repo = ParkingSpotRepository()

    # Create parking spots
    spots = [
        ParkingSpot(id="A-1", spot_number=1, spot_type=SpotType.SMALL),
        ParkingSpot(id="A-2", spot_number=2, spot_type=SpotType.SMALL),
        ParkingSpot(id="B-1", spot_number=3, spot_type=SpotType.MEDIUM),
        ParkingSpot(id="B-2", spot_number=4, spot_type=SpotType.MEDIUM),
        ParkingSpot(id="C-1", spot_number=5, spot_type=SpotType.LARGE),
    ]

    for spot in spots:
        spot_repo.save(spot)

    return spot_repo


def main():
    """Run the parking lot demo"""
    print("=" * 60)
    print("PARKING LOT SYSTEM DEMO")
    print("=" * 60)

    # Setup
    print("\n[SETUP] Initializing parking lot...")
    spot_repo = setup_parking_lot()
    vehicle_repo = VehicleRepository()
    ticket_repo = TicketRepository()
    payment_repo = PaymentRepository()

    allocation_strategy = NearestSpotStrategy()
    pricing_strategy = HourlyPricingStrategy()

    ticket_service = TicketService(
        spot_repo, vehicle_repo, ticket_repo, allocation_strategy
    )
    payment_service = PaymentService(
        payment_repo, ticket_repo, pricing_strategy
    )

    # Create gate and attendant
    entry_gate = ParkingGate(gate_id="GATE-1", gate_type=GateType.ENTRY)
    attendant = ParkingAttendant(
        id="ATD-1",
        name="Rajesh Kumar",
        email="rajesh@parking.com"
    )

    print(f"✓ Parking lot initialized with {len(spot_repo.find_all())} spots")
    print(f"✓ Attendant: {attendant.name}")

    # Scenario 1: Car Entry
    print("\n" + "-" * 60)
    print("[SCENARIO 1] Car arrives at parking lot")
    print("-" * 60)

    try:
        ticket1 = ticket_service.issue_ticket(
            license_plate="KA01AB1234",
            vehicle_type=VehicleType.CAR,
            entry_gate=entry_gate,
            entry_operator=attendant
        )
        print(f"✓ Ticket issued: {ticket1.ticket_id}")
        print(f"  - Vehicle: {ticket1.vehicle.license_plate}")
        print(f"  - Spot: {ticket1.parking_spot.id} ({ticket1.parking_spot.spot_type.value})")
        print(f"  - Entry time: {ticket1.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Scenario 2: Bike Entry
    print("\n" + "-" * 60)
    print("[SCENARIO 2] Bike arrives at parking lot")
    print("-" * 60)

    try:
        ticket2 = ticket_service.issue_ticket(
            license_plate="KA05XY9876",
            vehicle_type=VehicleType.BIKE,
            entry_gate=entry_gate,
            entry_operator=attendant
        )
        print(f"✓ Ticket issued: {ticket2.ticket_id}")
        print(f"  - Vehicle: {ticket2.vehicle.license_plate}")
        print(f"  - Spot: {ticket2.parking_spot.id} ({ticket2.parking_spot.spot_type.value})")
        print(f"  - Entry time: {ticket2.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Scenario 3: Check Available Spots
    print("\n" + "-" * 60)
    print("[SCENARIO 3] Check available spots")
    print("-" * 60)

    available = spot_repo.find_available()
    print(f"Available spots: {len(available)}")
    for spot in available:
        print(f"  - {spot.id}: {spot.spot_type.value} ({spot.status.value})")

    # Scenario 4: Payment for Car
    print("\n" + "-" * 60)
    print("[SCENARIO 4] Car owner makes payment")
    print("-" * 60)

    try:
        payment1 = payment_service.process_payment(
            ticket1.ticket_id,
            PaymentType.UPI
        )
        print(f"✓ Payment processed: {payment1.payment_id}")
        print(f"  - Amount: ₹{payment1.amount}")
        print(f"  - Method: {payment1.payment_type.value}")
        print(f"  - Status: {payment1.status.value}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Scenario 5: Generate Invoice and Exit
    print("\n" + "-" * 60)
    print("[SCENARIO 5] Generate invoice and exit")
    print("-" * 60)

    try:
        invoice = payment_service.generate_invoice(ticket1.ticket_id)
        print(f"✓ Invoice generated: {invoice.invoice_id}")
        print(f"  - Ticket: {invoice.ticket.ticket_id}")
        print(f"  - Entry: {invoice.ticket.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  - Exit: {invoice.exit_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  - Duration: ~1 hour")
        print(f"  - Amount: ₹{invoice.amount}")

        # Free the spot
        ticket_service.free_spot(ticket1.ticket_id)
        print(f"✓ Spot {invoice.ticket.parking_spot.id} is now FREE")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Scenario 6: Try to pay again (should fail)
    print("\n" + "-" * 60)
    print("[SCENARIO 6] Attempt duplicate payment (should fail)")
    print("-" * 60)

    try:
        payment_service.process_payment(ticket1.ticket_id, PaymentType.CASH)
        print("✗ Duplicate payment allowed (BUG!)")
    except Exception as e:
        print(f"✓ Correctly rejected: {e}")

    # Final status
    print("\n" + "=" * 60)
    print("FINAL STATUS")
    print("=" * 60)
    print(f"Total tickets issued: {len(ticket_repo.find_all())}")
    print(f"Total payments: {len(payment_repo.find_all())}")
    print(f"Available spots: {len(spot_repo.find_available())}/{len(spot_repo.find_all())}")

    print("\n✓ Demo completed successfully!")


if __name__ == "__main__":
    main()
