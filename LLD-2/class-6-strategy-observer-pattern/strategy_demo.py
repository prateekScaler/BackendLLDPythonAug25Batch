"""
Strategy Pattern Demo - Payment Processing System

This demonstrates the Strategy pattern with a shopping cart
that can switch payment methods at runtime.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ============================================
# STEP 1: Define the Strategy Interface
# ============================================

class PaymentStrategy(ABC):
    """Abstract base class for all payment strategies."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process payment and return success status."""
        pass


# ============================================
# STEP 2: Implement Concrete Strategies
# ============================================

class CreditCardStrategy(PaymentStrategy):
    """Pay using credit card."""

    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float) -> bool:
        # In real app: integrate with payment gateway
        print(f"💳 Paid ${amount:.2f} using Credit Card ending {self.card_number[-4:]}")
        return True


class PayPalStrategy(PaymentStrategy):
    """Pay using PayPal."""

    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> bool:
        # In real app: redirect to PayPal
        print(f"🅿️  Paid ${amount:.2f} using PayPal ({self.email})")
        return True


class CryptoStrategy(PaymentStrategy):
    """Pay using cryptocurrency."""

    def __init__(self, wallet_address: str):
        self.wallet = wallet_address

    def pay(self, amount: float) -> bool:
        # In real app: send blockchain transaction
        print(f"₿  Paid ${amount:.2f} using Crypto wallet {self.wallet[:8]}...")
        return True


class UPIStrategy(PaymentStrategy):
    """Pay using UPI (India)."""

    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def pay(self, amount: float) -> bool:
        print(f"📱 Paid ${amount:.2f} using UPI ({self.upi_id})")
        return True


# ============================================
# STEP 3: Create the Context
# ============================================

class ShoppingCart:
    """Shopping cart that uses strategy for payment."""

    def __init__(self):
        self.items: list[tuple[str, float]] = []
        self._payment_strategy: PaymentStrategy | None = None

    def add_item(self, name: str, price: float):
        """Add item to cart."""
        self.items.append((name, price))
        print(f"Added: {name} - ${price:.2f}")

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """Set or change payment method at runtime."""
        self._payment_strategy = strategy

    def get_total(self) -> float:
        """Calculate total price."""
        return sum(price for _, price in self.items)

    def checkout(self) -> bool:
        """Process checkout using selected payment strategy."""
        if not self._payment_strategy:
            raise ValueError("❌ No payment method selected!")

        if not self.items:
            raise ValueError("❌ Cart is empty!")

        total = self.get_total()
        print(f"\n🛒 Checking out {len(self.items)} items (Total: ${total:.2f})")

        success = self._payment_strategy.pay(total)

        if success:
            print("✅ Payment successful!")
            self.items.clear()

        return success


# ============================================
# DEMO
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("STRATEGY PATTERN DEMO - Payment System")
    print("=" * 50)

    # Create shopping cart
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99)
    cart.add_item("Keyboard", 79.99)

    # Scenario 1: Pay with Credit Card
    print("\n--- Scenario 1: Credit Card ---")
    cart.set_payment_strategy(
        CreditCardStrategy("4532015112830366", "123")
    )
    cart.checkout()

    # Add more items
    cart.add_item("Monitor", 299.99)
    cart.add_item("Webcam", 89.99)

    # Scenario 2: User changes mind - Pay with PayPal
    print("\n--- Scenario 2: Switch to PayPal ---")
    cart.set_payment_strategy(
        PayPalStrategy("user@example.com")
    )
    cart.checkout()

    # Add more items
    cart.add_item("Headphones", 149.99)

    # Scenario 3: Pay with Crypto
    print("\n--- Scenario 3: Switch to Crypto ---")
    cart.set_payment_strategy(
        CryptoStrategy("0x742d35Cc6634C0532925a3b844Bc9e7595f...")
    )
    cart.checkout()

    # Scenario 4: New payment method - UPI (no code changes!)
    cart.add_item("USB Hub", 24.99)
    print("\n--- Scenario 4: New Method - UPI ---")
    cart.set_payment_strategy(
        UPIStrategy("user@okbank")
    )
    cart.checkout()

    print("\n" + "=" * 50)
    print("KEY TAKEAWAY: Changed payment methods without")
    print("modifying ShoppingCart class!")
    print("=" * 50)