"""
SOLID Principles - Complete E-commerce Example
Evolution from bad design to SOLID design
"""

print("=" * 60)
print("SOLID PRINCIPLES - PRACTICAL EVOLUTION")
print("=" * 60)

# ============================================================================
# BEFORE: Violates ALL SOLID Principles
# ============================================================================

print("\n❌ BAD DESIGN (Violates SOLID)")
print("-" * 60)


class Order:
    def __init__(self, items):
        self.items = items
        self.status = "pending"

    def process_order(self):
        # SRP Violation: Does everything
        # Calculate total
        total = sum(item['price'] * item['qty'] for item in self.items)

        # Apply discount
        if total > 100:
            total *= 0.9

        # OCP Violation: Must modify to add payment methods
        payment_method = "credit_card"
        if payment_method == "credit_card":
            print(f"Charging ${total} to card")
        elif payment_method == "paypal":
            print(f"Charging ${total} to PayPal")

        # DIP Violation: Direct dependency on MySQL
        import mysql.connector
        db = mysql.connector.connect(host="localhost")
        db.cursor().execute(f"INSERT INTO orders VALUES ({total})")

        # Send email
        import smtplib
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.send(f"Order total: ${total}")

        print(f"Order processed: ${total}")


# Problems:
# - Can't test without real DB/SMTP
# - Must modify class to add payment methods
# - Tightly coupled
# - Does too many things

print("Problems:")
print("  • Violates SRP: Does calculation, payment, DB, email")
print("  • Violates OCP: Must modify to add payment methods")
print("  • Violates DIP: Direct dependencies on MySQL, SMTP")
print("  • Hard to test, inflexible")

# ============================================================================
# AFTER: Follows SOLID Principles
# ============================================================================

print("\n✅ GOOD DESIGN (Follows SOLID)")
print("-" * 60)

from abc import ABC, abstractmethod


# SRP: Separate responsibilities
class Order:
    """Domain model - only order data"""

    def __init__(self, items):
        self.items = items
        self.status = "pending"

    def calculate_total(self):
        return sum(item['price'] * item['qty'] for item in self.items)


class DiscountCalculator:
    """SRP: Only calculates discounts"""

    def apply(self, total):
        if total > 100:
            return total * 0.9
        return total


# OCP & DIP: Abstractions for extension
class PaymentMethod(ABC):
    """OCP: Open for extension"""

    @abstractmethod
    def process(self, amount):
        pass


class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        return f"Charged ${amount} to card"


class PayPalPayment(PaymentMethod):
    def process(self, amount):
        return f"Charged ${amount} via PayPal"


class CryptoPayment(PaymentMethod):  # Easy to add new method!
    def process(self, amount):
        return f"Charged ${amount} in crypto"


# DIP: Abstract database
class OrderRepository(ABC):
    """DIP: High-level doesn't depend on low-level"""

    @abstractmethod
    def save(self, order):
        pass


class MySQLRepository(OrderRepository):
    def save(self, order):
        return f"Saved order to MySQL"


class PostgreSQLRepository(OrderRepository):  # Easy to switch!
    def save(self, order):
        return f"Saved order to PostgreSQL"


# DIP: Abstract notifications
class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailNotifier(Notifier):
    def send(self, message):
        return f"Email sent: {message}"


class SMSNotifier(Notifier):  # Easy to add!
    def send(self, message):
        return f"SMS sent: {message}"


# SRP: Orchestrates but doesn't do everything
class OrderProcessor:
    """SRP: Coordinates order processing"""

    def __init__(
            self,
            repository: OrderRepository,
            notifier: Notifier,
            discount_calculator: DiscountCalculator
    ):
        # DIP: Depends on abstractions
        self.repository = repository
        self.notifier = notifier
        self.discount_calculator = discount_calculator

    def process(self, order: Order, payment: PaymentMethod):
        # Calculate
        total = order.calculate_total()
        total = self.discount_calculator.apply(total)

        # Process payment (OCP: accepts any payment method)
        result = payment.process(total)
        print(f"  {result}")

        # Save (DIP: doesn't care which database)
        save_result = self.repository.save(order)
        print(f"  {save_result}")

        # Notify (DIP: doesn't care which channel)
        notify_result = self.notifier.send(f"Order total: ${total}")
        print(f"  {notify_result}")


# ============================================================================
# DEMONSTRATION
# ============================================================================

print("\nDemonstration:")
print("-" * 60)

# Create order
order = Order([
    {'price': 50, 'qty': 2},
    {'price': 30, 'qty': 1}
])

# Configure dependencies (DIP: Dependency Injection)
repository = MySQLRepository()
notifier = EmailNotifier()
discount = DiscountCalculator()

processor = OrderProcessor(repository, notifier, discount)

# Process with credit card
print("\n1. Processing with Credit Card:")
payment = CreditCardPayment()
processor.process(order, payment)

# Easy to switch payment method (OCP)
print("\n2. Processing with PayPal:")
payment = PayPalPayment()
processor.process(order, payment)

# Easy to add new payment (OCP)
print("\n3. Processing with Crypto:")
payment = CryptoPayment()
processor.process(order, payment)

# Easy to switch database (DIP)
print("\n4. Switching to PostgreSQL:")
processor.repository = PostgreSQLRepository()
processor.process(order, CreditCardPayment())

# Easy to add SMS notifications (OCP + DIP)
print("\n5. Adding SMS notifications:")
processor.notifier = SMSNotifier()
processor.process(order, PayPalPayment())

# ============================================================================
# BENEFITS DEMONSTRATED
# ============================================================================

print("\n" + "=" * 60)
print("BENEFITS")
print("=" * 60)
print("""
✅ Single Responsibility (SRP):
   • Order: Just data
   • DiscountCalculator: Just discounts
   • OrderProcessor: Just coordination
   • Each class has one reason to change

✅ Open/Closed (OCP):
   • Add new payment methods without modifying processor
   • Add new notification channels without changes
   • Extended through new classes, not modifications

✅ Liskov Substitution (LSP):
   • Any PaymentMethod works in processor
   • Any Repository works in processor
   • Any Notifier works in processor

✅ Interface Segregation (ISP):
   • Small, focused interfaces (PaymentMethod, Repository, Notifier)
   • Clients depend only on what they use

✅ Dependency Inversion (DIP):
   • Processor depends on abstractions
   • Easy to swap implementations
   • Testable with mocks

🎯 Overall Benefits:
   • Flexible: Easy to add features
   • Testable: Can mock all dependencies
   • Maintainable: Changes isolated
   • Reusable: Components independent
""")

# ============================================================================
# TESTING EXAMPLE
# ============================================================================

print("=" * 60)
print("TESTING BENEFITS")
print("=" * 60)


# Easy to create test doubles
class FakeRepository(OrderRepository):
    def save(self, order):
        return "Saved to fake DB"


class FakeNotifier(Notifier):
    def send(self, message):
        return "Sent fake notification"


class FakePayment(PaymentMethod):
    def process(self, amount):
        return f"Fake payment of ${amount}"


# Test without real dependencies
print("\nTesting with fakes:")
test_processor = OrderProcessor(
    FakeRepository(),
    FakeNotifier(),
    DiscountCalculator()
)

test_order = Order([{'price': 10, 'qty': 1}])
test_processor.process(test_order, FakePayment())

print("\n✅ Testing is easy - no real DB, SMTP, or payment gateway needed!")

print("\n" + "=" * 60)
print("KEY TAKEAWAY")
print("=" * 60)
print("""
SOLID principles work together to create:
  • Flexible systems (easy to extend)
  • Maintainable code (easy to change)
  • Testable components (easy to verify)
  • Reusable modules (easy to compose)

Start with SRP, add OCP for extension, ensure LSP for inheritance,
apply ISP for focused interfaces, and use DIP for flexibility.
""")