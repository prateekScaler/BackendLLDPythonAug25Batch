"""
Observer Pattern Demo - Stock Price Notification System

This demonstrates the Observer pattern with a stock ticker
that notifies multiple observers when prices change.
"""

from abc import ABC, abstractmethod


# ============================================
# STEP 1: Define the Observer Interface
# ============================================

class Observer(ABC):
    """Abstract base class for all observers."""

    @abstractmethod
    def update(self, data: dict) -> None:
        """Called when subject state changes."""
        pass


# ============================================
# STEP 2: Define the Subject Interface
# ============================================

class Subject(ABC):
    """Abstract base class for subjects (observables)."""

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Subscribe an observer."""
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Unsubscribe an observer."""
        pass

    @abstractmethod
    def notify(self) -> None:
        """Notify all observers of state change."""
        pass


# ============================================
# STEP 3: Implement Concrete Subject
# ============================================

class StockTicker(Subject):
    """Stock ticker that notifies observers of price changes."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self._price = 0.0
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"📎 {observer.__class__.__name__} subscribed to {self.symbol}")

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"📌 {observer.__class__.__name__} unsubscribed from {self.symbol}")

    def notify(self) -> None:
        for observer in self._observers:
            observer.update({
                "symbol": self.symbol,
                "price": self._price
            })

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        old_price = self._price
        self._price = value
        change = "📈" if value > old_price else "📉" if value < old_price else "➡️"
        print(f"\n{change} {self.symbol}: ${old_price:.2f} → ${value:.2f}")
        self.notify()


# ============================================
# STEP 4: Implement Concrete Observers
# ============================================

class DashboardDisplay(Observer):
    """Updates a dashboard UI with stock prices."""

    def update(self, data: dict) -> None:
        print(f"   🖥️  Dashboard: {data['symbol']} is now ${data['price']:.2f}")


class MobileApp(Observer):
    """Sends push notifications to mobile app."""

    def __init__(self, user_id: str = "user123"):
        self.user_id = user_id

    def update(self, data: dict) -> None:
        print(f"   📱 Push to {self.user_id}: {data['symbol']} = ${data['price']:.2f}")


class TradingBot(Observer):
    """Automated trading bot that reacts to price changes."""

    def __init__(self, buy_threshold: float, sell_threshold: float):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def update(self, data: dict) -> None:
        price = data['price']
        symbol = data['symbol']

        if price < self.buy_threshold:
            print(f"   🤖 Bot: 🟢 BUY {symbol} @ ${price:.2f} (< ${self.buy_threshold})")
        elif price > self.sell_threshold:
            print(f"   🤖 Bot: 🔴 SELL {symbol} @ ${price:.2f} (> ${self.sell_threshold})")
        else:
            print(f"   🤖 Bot: ⚪ HOLD {symbol} @ ${price:.2f}")


class EmailAlert(Observer):
    """Sends email alerts when price exceeds threshold."""

    def __init__(self, email: str, threshold: float):
        self.email = email
        self.threshold = threshold
        self._alerted = False

    def update(self, data: dict) -> None:
        price = data['price']
        symbol = data['symbol']

        if price > self.threshold and not self._alerted:
            print(f"   📧 Email to {self.email}: ⚠️ {symbol} exceeded ${self.threshold}!")
            self._alerted = True
        elif price <= self.threshold:
            self._alerted = False  # Reset alert


class PriceLogger(Observer):
    """Logs all price changes for analysis."""

    def __init__(self):
        self.history: list[tuple[str, float]] = []

    def update(self, data: dict) -> None:
        self.history.append((data['symbol'], data['price']))
        print(f"   📝 Logged: {data['symbol']} @ ${data['price']:.2f} (#{len(self.history)})")


# ============================================
# DEMO
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("OBSERVER PATTERN DEMO - Stock Price Notification System")
    print("=" * 60)

    # Create subject (stock ticker)
    apple = StockTicker("AAPL")

    # Create observers
    dashboard = DashboardDisplay()
    mobile = MobileApp("trader_Mudit")
    bot = TradingBot(buy_threshold=145, sell_threshold=165)
    email = EmailAlert("Mudit@trader.com", threshold=160)
    logger = PriceLogger()

    # Subscribe observers
    print("\n--- Subscribing Observers ---")
    apple.attach(dashboard)
    apple.attach(mobile)
    apple.attach(bot)
    apple.attach(email)
    apple.attach(logger)

    # Simulate price changes
    print("\n--- Price Changes (all observers notified) ---")
    apple.price = 150.00  # Initial price
    apple.price = 155.00  # Price increase
    apple.price = 162.00  # Above email threshold!
    apple.price = 168.00  # Above sell threshold!

    # User disables mobile notifications
    print("\n--- Mobile User Disabled Notifications ---")
    apple.detach(mobile)

    apple.price = 142.00  # Price drop - mobile won't receive
    apple.price = 140.00  # Below buy threshold!

    # Show logged history
    print("\n--- Price History Log ---")
    for symbol, price in logger.history:
        print(f"   {symbol}: ${price:.2f}")

    print("\n" + "=" * 60)
    print("KEY TAKEAWAY: Subject doesn't know who observers are.")
    print("Observers can be added/removed dynamically!")
    print("=" * 60)