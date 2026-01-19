"""
mocking_basics.py
=================
Real-world mocking examples for an e-commerce application.

This module contains:
1. Service classes that depend on external systems
2. Examples of what we need to mock in tests

Run: python mocking_basics.py
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum
import time


# ============================================================
# EXTERNAL DEPENDENCIES (Things we'll mock in tests)
# ============================================================

class PaymentGateway:
    """
    Real payment gateway - connects to Razorpay/Stripe.
    In tests, we MOCK this to avoid real charges!
    """

    def charge(self, card_number: str, amount: float, currency: str = "INR") -> dict:
        """Charge a card - THIS WOULD HIT REAL API"""
        # In reality, this calls external API
        # We don't want tests to charge real cards!
        print(f"[REAL API] Charging {amount} {currency} to card {card_number[-4:]}")
        time.sleep(2)  # Simulates network latency
        return {
            "status": "success",
            "transaction_id": "txn_real_123",
            "amount": amount
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        """Refund a transaction"""
        print(f"[REAL API] Refunding {amount} for {transaction_id}")
        time.sleep(1)
        return {"status": "refunded", "refund_id": "ref_real_456"}


class EmailService:
    """
    Real email service - sends actual emails via SMTP/SendGrid.
    In tests, we MOCK this to avoid spam!
    """

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email - THIS WOULD SEND REAL EMAIL"""
        print(f"[REAL EMAIL] Sending to {to}: {subject}")
        time.sleep(0.5)
        return True

    def send_bulk_email(self, recipients: List[str], subject: str, body: str) -> int:
        """Send bulk email - returns count of sent emails"""
        print(f"[REAL EMAIL] Sending to {len(recipients)} recipients")
        time.sleep(len(recipients) * 0.1)
        return len(recipients)


class InventoryService:
    """
    Real inventory service - checks/updates stock in database.
    In tests, we MOCK this to avoid database dependencies!
    """

    def check_stock(self, product_id: str) -> int:
        """Check available stock"""
        print(f"[REAL DB] Checking stock for {product_id}")
        time.sleep(0.3)
        return 100  # Simulated stock

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Reserve stock for an order"""
        print(f"[REAL DB] Reserving {quantity} units of {product_id}")
        time.sleep(0.2)
        return True

    def release_stock(self, product_id: str, quantity: int) -> bool:
        """Release reserved stock"""
        print(f"[REAL DB] Releasing {quantity} units of {product_id}")
        return True


class NotificationService:
    """SMS/Push notification service"""

    def send_sms(self, phone: str, message: str) -> bool:
        """Send SMS - costs money per message!"""
        print(f"[REAL SMS] Sending to {phone}: {message[:20]}...")
        time.sleep(0.5)
        return True

    def send_push(self, user_id: str, title: str, body: str) -> bool:
        """Send push notification"""
        print(f"[REAL PUSH] Sending to user {user_id}")
        return True


# ============================================================
# BUSINESS LOGIC (The code we're actually testing)
# ============================================================

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    REFUNDED = "refunded"


@dataclass
class Order:
    id: str
    user_email: str
    user_phone: str
    product_id: str
    quantity: int
    amount: float
    status: OrderStatus = OrderStatus.PENDING
    transaction_id: Optional[str] = None


class OrderService:
    """
    Order processing service - THIS is what we want to test.

    Dependencies:
    - PaymentGateway (external API)
    - EmailService (external service)
    - InventoryService (database)
    - NotificationService (external service)

    In tests, we mock all dependencies to test OrderService in isolation.
    """

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        email_service: EmailService,
        inventory_service: InventoryService,
        notification_service: NotificationService
    ):
        self.payment = payment_gateway
        self.email = email_service
        self.inventory = inventory_service
        self.notification = notification_service

    def place_order(self, order: Order) -> Order:
        """
        Place an order - the main business logic we want to test.

        Steps:
        1. Check inventory
        2. Reserve stock
        3. Process payment
        4. Send confirmation email
        5. Send SMS notification

        If any step fails, we need to rollback previous steps.
        """

        # Step 1: Check inventory
        available_stock = self.inventory.check_stock(order.product_id)
        if available_stock < order.quantity:
            order.status = OrderStatus.FAILED
            raise ValueError(f"Insufficient stock. Available: {available_stock}")

        # Step 2: Reserve stock
        if not self.inventory.reserve_stock(order.product_id, order.quantity):
            order.status = OrderStatus.FAILED
            raise ValueError("Failed to reserve stock")

        try:
            # Step 3: Process payment
            payment_result = self.payment.charge(
                card_number="4111111111111111",  # Would come from request
                amount=order.amount
            )

            if payment_result["status"] != "success":
                raise ValueError("Payment failed")

            order.transaction_id = payment_result["transaction_id"]
            order.status = OrderStatus.CONFIRMED

            # Step 4: Send confirmation email
            self.email.send_email(
                to=order.user_email,
                subject=f"Order {order.id} Confirmed!",
                body=f"Your order for {order.quantity} items is confirmed."
            )

            # Step 5: Send SMS notification
            self.notification.send_sms(
                phone=order.user_phone,
                message=f"Order {order.id} confirmed! Amount: Rs.{order.amount}"
            )

            return order

        except Exception as e:
            # Rollback: Release reserved stock
            self.inventory.release_stock(order.product_id, order.quantity)
            order.status = OrderStatus.FAILED
            raise

    def refund_order(self, order: Order) -> Order:
        """Refund an order"""
        if order.status != OrderStatus.CONFIRMED:
            raise ValueError(f"Cannot refund order in {order.status} status")

        if not order.transaction_id:
            raise ValueError("No transaction to refund")

        # Process refund
        refund_result = self.payment.refund(order.transaction_id, order.amount)

        if refund_result["status"] == "refunded":
            # Release stock
            self.inventory.release_stock(order.product_id, order.quantity)

            # Notify user
            self.email.send_email(
                to=order.user_email,
                subject=f"Order {order.id} Refunded",
                body=f"Your refund of Rs.{order.amount} has been processed."
            )

            order.status = OrderStatus.REFUNDED

        return order

    def get_order_summary(self, order: Order) -> dict:
        """Get order summary - no external calls, no need to mock"""
        return {
            "order_id": order.id,
            "status": order.status.value,
            "amount": order.amount,
            "quantity": order.quantity
        }


# ============================================================
# DEMONSTRATION - Why mocking matters
# ============================================================

def demonstrate_without_mocking():
    """
    Running tests WITHOUT mocking - see the problems:
    - Slow (network calls)
    - Side effects (real emails, real charges)
    - Unreliable (network failures)
    """
    print("=" * 60)
    print("WITHOUT MOCKING - Real dependencies")
    print("=" * 60)

    # Create real services
    payment = PaymentGateway()
    email = EmailService()
    inventory = InventoryService()
    notification = NotificationService()

    order_service = OrderService(payment, email, inventory, notification)

    order = Order(
        id="ORD-001",
        user_email="user@example.com",
        user_phone="9876543210",
        product_id="PROD-123",
        quantity=2,
        amount=999.00
    )

    print("\nPlacing order (watch the real API calls!)...")
    print("-" * 60)

    start = time.time()
    try:
        result = order_service.place_order(order)
        print(f"\nOrder status: {result.status}")
    except Exception as e:
        print(f"\nOrder failed: {e}")

    elapsed = time.time() - start
    print(f"\nTime taken: {elapsed:.2f} seconds")
    print("^ This is TOO SLOW for unit tests!")
    print("^ Also sent REAL emails/SMS (costs money!)")


def demonstrate_test_scenarios():
    """Show the scenarios we need to test (with mocking)"""
    print("\n" + "=" * 60)
    print("SCENARIOS WE NEED TO TEST (with mocking)")
    print("=" * 60)

    scenarios = [
        ("Happy path", "Everything succeeds"),
        ("Insufficient stock", "Inventory check fails"),
        ("Payment failure", "Card declined"),
        ("Payment timeout", "Gateway doesn't respond"),
        ("Email failure", "SMTP server down"),
        ("Partial failure", "Payment succeeds, email fails - should we rollback?"),
        ("Refund success", "Full refund flow"),
        ("Refund failure", "Refund API fails"),
        ("Concurrent orders", "Race condition on last item"),
    ]

    print("\nTo test these scenarios, we need to MOCK dependencies:")
    print("-" * 60)

    for i, (scenario, description) in enumerate(scenarios, 1):
        print(f"{i}. {scenario}: {description}")

    print("""
Without mocking, how would you test "Payment timeout"?
- Can't make real Razorpay timeout on demand
- Would need to wait for actual timeouts (slow!)

With mocking:
    mock_payment.charge.side_effect = TimeoutError("Gateway timeout")

Now you can test ANY scenario instantly!
    """)


# ============================================================
# RUN DEMONSTRATIONS
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  MOCKING DEMONSTRATION")
    print("  Why we mock external dependencies in tests")
    print("=" * 60 + "\n")

    # Uncomment to see real API calls (slow!)
    # demonstrate_without_mocking()

    demonstrate_test_scenarios()

    print("\n" + "=" * 60)
    print("Next: See test_mocking_basics.py for mocked tests!")
    print("=" * 60)
