"""
Decorator Pattern Demo - Coffee Shop Order System

This demonstrates how decorators allow adding responsibilities
to objects dynamically without class explosion.
"""

from abc import ABC, abstractmethod


# ============================================
# STEP 1: Component Interface
# ============================================

class Beverage(ABC):
    """Base component interface for all beverages"""

    @abstractmethod
    def cost(self) -> float:
        """Return the cost of the beverage"""
        pass

    @abstractmethod
    def description(self) -> str:
        """Return the description of the beverage"""
        pass


# ============================================
# STEP 2: Concrete Components (Base Beverages)
# ============================================

class Coffee(Beverage):
    """Concrete component - basic coffee"""

    def cost(self) -> float:
        return 5.0

    def description(self) -> str:
        return "Coffee"


class Tea(Beverage):
    """Concrete component - basic tea"""

    def cost(self) -> float:
        return 3.0

    def description(self) -> str:
        return "Tea"


class HotChocolate(Beverage):
    """Concrete component - basic hot chocolate"""

    def cost(self) -> float:
        return 4.5

    def description(self) -> str:
        return "Hot Chocolate"


# ============================================
# STEP 3: Decorator Base Class
# ============================================

class AddOnDecorator(Beverage):
    """
    Base decorator class that wraps a Beverage.
    Maintains the same interface as Beverage.
    """

    def __init__(self, beverage: Beverage):
        self._beverage = beverage

    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


# ============================================
# STEP 4: Concrete Decorators (Add-ons)
# ============================================

class Milk(AddOnDecorator):
    """Decorator - adds milk"""

    def cost(self) -> float:
        return self._beverage.cost() + 1.5

    def description(self) -> str:
        return self._beverage.description() + " + Milk"


class Sugar(AddOnDecorator):
    """Decorator - adds sugar"""

    def cost(self) -> float:
        return self._beverage.cost() + 0.5

    def description(self) -> str:
        return self._beverage.description() + " + Sugar"


class WhippedCream(AddOnDecorator):
    """Decorator - adds whipped cream"""

    def cost(self) -> float:
        return self._beverage.cost() + 2.0

    def description(self) -> str:
        return self._beverage.description() + " + Whipped Cream"


class Caramel(AddOnDecorator):
    """Decorator - adds caramel"""

    def cost(self) -> float:
        return self._beverage.cost() + 1.0

    def description(self) -> str:
        return self._beverage.description() + " + Caramel"


class Vanilla(AddOnDecorator):
    """Decorator - adds vanilla"""

    def cost(self) -> float:
        return self._beverage.cost() + 0.75

    def description(self) -> str:
        return self._beverage.description() + " + Vanilla"


class Cinnamon(AddOnDecorator):
    """Decorator - adds cinnamon"""

    def cost(self) -> float:
        return self._beverage.cost() + 0.60

    def description(self) -> str:
        return self._beverage.description() + " + Cinnamon"


# ============================================
# HELPER FUNCTION
# ============================================

def print_order(beverage: Beverage):
    """Pretty print order details"""
    print(f"{'─' * 50}")
    print(f"Order: {beverage.description()}")
    print(f"Total Cost: ${beverage.cost():.2f}")
    print(f"{'─' * 50}\n")


# ============================================
# DEMO
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("DECORATOR PATTERN DEMO - Coffee Shop")
    print("=" * 50)
    print()

    # ===== Scenario 1: Simple Coffee =====
    print("📋 Order 1: Simple Coffee")
    order1 = Coffee()
    print_order(order1)

    # ===== Scenario 2: Coffee with Milk =====
    print("📋 Order 2: Coffee with Milk")
    order2 = Coffee()
    order2 = Milk(order2)  # Wrap with Milk decorator
    print_order(order2)

    # ===== Scenario 3: Coffee with Multiple Add-ons =====
    print("📋 Order 3: Coffee with Milk, Sugar, and Whipped Cream")
    order3 = Coffee()
    order3 = Milk(order3)
    order3 = Sugar(order3)
    order3 = WhippedCream(order3)
    print_order(order3)

    # ===== Scenario 4: Fancy Latte (Double Milk!) =====
    print("📋 Order 4: Extra Creamy Latte (Double Milk + Vanilla)")
    order4 = Coffee()
    order4 = Milk(order4)
    order4 = Milk(order4)  # Can add same decorator twice!
    order4 = Vanilla(order4)
    print_order(order4)

    # ===== Scenario 5: Caramel Macchiato =====
    print("📋 Order 5: Caramel Macchiato")
    order5 = Coffee()
    order5 = Milk(order5)
    order5 = Caramel(order5)
    order5 = Vanilla(order5)
    order5 = WhippedCream(order5)
    print_order(order5)

    # ===== Scenario 6: Tea with Honey (represented by Sugar) =====
    print("📋 Order 6: Tea with Sugar and Cinnamon")
    order6 = Tea()
    order6 = Sugar(order6)
    order6 = Cinnamon(order6)
    print_order(order6)

    # ===== Scenario 7: Hot Chocolate Deluxe =====
    print("📋 Order 7: Hot Chocolate Deluxe")
    order7 = HotChocolate()
    order7 = WhippedCream(order7)
    order7 = Caramel(order7)
    order7 = Cinnamon(order7)
    print_order(order7)

    # ===== Scenario 8: Everything! =====
    print("📋 Order 8: The Kitchen Sink (Everything!)")
    order8 = Coffee()
    order8 = Milk(order8)
    order8 = Sugar(order8)
    order8 = WhippedCream(order8)
    order8 = Caramel(order8)
    order8 = Vanilla(order8)
    order8 = Cinnamon(order8)
    print_order(order8)

    # ===== Demonstrate Flexibility =====
    print("\n" + "=" * 50)
    print("ADDING NEW ADD-ON WITHOUT MODIFYING EXISTING CODE")
    print("=" * 50)
    print()


    # Imagine this is added later (Open/Closed Principle)
    class Hazelnut(AddOnDecorator):
        """NEW decorator - adds hazelnut"""

        def cost(self) -> float:
            return self._beverage.cost() + 1.25

        def description(self) -> str:
            return self._beverage.description() + " + Hazelnut"


    print("📋 Order 9: Coffee with NEW Hazelnut add-on")
    order9 = Coffee()
    order9 = Hazelnut(order9)  # Use new decorator!
    order9 = Milk(order9)
    print_order(order9)

    # ===== Show the Nesting =====
    print("=" * 50)
    print("VISUALIZATION: How Decorators Wrap")
    print("=" * 50)
    print()
    print("Order: Coffee + Milk + Sugar + Whipped Cream")
    print()
    print("Structure:")
    print("WhippedCream(")
    print("    Sugar(")
    print("        Milk(")
    print("            Coffee()")
    print("        )")
    print("    )")
    print(")")
    print()
    print("Cost Calculation (from inside out):")
    print("1. Coffee.cost() = 5.0")
    print("2. Milk.cost() = Coffee.cost() + 1.5 = 6.5")
    print("3. Sugar.cost() = Milk.cost() + 0.5 = 7.0")
    print("4. WhippedCream.cost() = Sugar.cost() + 2.0 = 9.0")
    print()

    # ===== Final Summary =====
    print("=" * 50)
    print("KEY BENEFITS DEMONSTRATED")
    print("=" * 50)
    print("✅ No class explosion - 6 decorators, infinite combinations")
    print("✅ Can add same decorator multiple times (double milk)")
    print("✅ Easy to add new decorators (Hazelnut) without modifying existing code")
    print("✅ Flexible runtime composition")
    print("✅ Each decorator has single responsibility")
    print("=" * 50)