# Adapter Design Pattern

## 📖 Definition

**"Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces."**

**In simpler terms:** Make incompatible interfaces work together by creating a wrapper that translates one interface to another.

---

## 🎯 The Problem

### Scenario: Third-Party SDK Integration

**The REALISTIC scenario:**

```python
# ALL payment gateways are third-party SDKs with different interfaces!

# Stripe SDK (third-party - can't modify)
class StripeSDK:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def create_charge(self, amount_cents: int, currency: str = "usd") -> StripeCharge:
        """Stripe's actual method"""
        return StripeCharge(
            id=f"ch_{amount_cents}",
            paid=True,
            amount=amount_cents
        )

class StripeCharge:
    def __init__(self, id: str, paid: bool, amount: int):
        self.id = id
        self.paid = paid
        self.amount = amount


# PayPal SDK (third-party - can't modify)
class PayPalSDK:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def execute_payment(self, payment_data: dict) -> PayPalPayment:
        """PayPal's actual method"""
        return PayPalPayment(
            state="approved",
            payment_id=f"PAY-{payment_data['amount']}"
        )

class PayPalPayment:
    def __init__(self, state: str, payment_id: str):
        self.state = state
        self.payment_id = payment_id


# Square SDK (third-party - can't modify)
class SquareSDK:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def charge_card(self, amount_in_cents: int, card_token: str) -> SquareResponse:
        """Square's actual method"""
        return SquareResponse(
            status="SUCCESS",
            transaction_id=f"sq_{amount_in_cents}"
        )

class SquareResponse:
    def __init__(self, status: str, transaction_id: str):
        self.status = status
        self.transaction_id = transaction_id
```

---

**Your application needs a UNIFIED interface:**

```python
# YOUR application's interface (what YOUR code expects)
class PaymentGatewayAdapter(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        """
        Standard interface for YOUR application
        - Takes amount in DOLLARS (float)
        - Returns dict with 'success' and 'transaction_id'
        """
        pass


# Your business logic expects THIS interface
def checkout(gateway: PaymentGateway, amount: float):
    """Your application code - expects PaymentGateway interface"""
    result = gateway.process_payment(amount)  # Expects this method!
    
    if result["success"]:  # Expects this dict format!
        print(f"✅ Payment successful: {result['transaction_id']}")
        send_confirmation_email(result)
        update_inventory()
    else:
        print("❌ Payment failed")
    
    return result
```

---

**Why can't you use the SDKs directly?**

```python
# Try using Stripe SDK directly
stripe_sdk = StripeSDK("sk_test_123")
checkout(stripe_sdk, 100.00)  # 💥 FAILS!

# Problem 1: StripeSDK doesn't inherit from PaymentGateway
# Problem 2: No process_payment() method - has create_charge() instead
# Problem 3: Different parameters - needs cents, not dollars
# Problem 4: Returns StripeCharge object, not dict
# Problem 5: Success field is .paid, not result["success"]


# Try using PayPal SDK directly
paypal_sdk = PayPalSDK("client_123", "secret_456")
checkout(paypal_sdk, 100.00)  # 💥 FAILS!

# Problem 1: PayPalSDK doesn't inherit from PaymentGateway
# Problem 2: No process_payment() method - has execute_payment() instead
# Problem 3: Needs dict parameter, not float
# Problem 4: Returns PayPalPayment object, not dict
# Problem 5: Success field is .state == "approved", not result["success"]


# Try using Square SDK directly
square_sdk = SquareSDK("api_key_789")
checkout(square_sdk, 100.00)  # 💥 FAILS!

# Problem 1: SquareSDK doesn't inherit from PaymentGateway
# Problem 2: No process_payment() method - has charge_card() instead
# Problem 3: Needs cents AND card_token, not just dollars
# Problem 4: Returns SquareResponse object, not dict
# Problem 5: Success field is .status == "SUCCESS", not result["success"]
```

**Problems:**
- ❌ Interface incompatibility (different method names)
- ❌ Parameter mismatch (dollars vs cents, different arguments)
- ❌ Return type mismatch (dict vs custom objects)
- ❌ Can't modify third-party SDKs (external libraries)
- ❌ Don't want to modify existing code (checkout function)

---

## ✅ The Solution: Adapter Pattern

**Create adapters that implement the expected interface and translate calls to the incompatible SDKs.**

```python
# Stripe Adapter
class StripeAdapter(PaymentGatewayAdapter):
    def __init__(self, secret_key: str):
        self.sdk = StripeSDK(secret_key)  # Wrap the SDK
    
    def process_payment(self, amount: float) -> dict:
        # Translate YOUR interface → Stripe's interface
        amount_cents = int(amount * 100)  # Convert dollars to cents
        charge = self.sdk.create_charge(amount_cents)  # Call Stripe's method
        
        # Translate Stripe's response → YOUR format
        return {
            "success": charge.paid,
            "transaction_id": charge.id
        }


# PayPal Adapter
class PayPalAdapter(PaymentGatewayAdapter):
    def __init__(self, client_id: str, client_secret: str):
        self.sdk = PayPalSDK(client_id, client_secret)  # Wrap the SDK
    
    def process_payment(self, amount: float) -> dict:
        # Translate YOUR interface → PayPal's interface
        payment_data = {"amount": amount, "currency": "USD"}
        payment = self.sdk.execute_payment(payment_data)  # Call PayPal's method
        
        # Translate PayPal's response → YOUR format
        return {
            "success": payment.state == "approved",
            "transaction_id": payment.payment_id
        }


# Square Adapter
class SquareAdapter(PaymentGatewayAdapter):
    def __init__(self, api_key: str):
        self.sdk = SquareSDK(api_key)  # Wrap the SDK
    
    def process_payment(self, amount: float) -> dict:
        # Translate YOUR interface → Square's interface
        amount_cents = int(amount * 100)
        response = self.sdk.charge_card(amount_cents, "card_nonce_123")  # Call Square's method
        
        # Translate Square's response → YOUR format
        return {
            "success": response.status == "SUCCESS",
            "transaction_id": response.transaction_id
        }
```

---

**Now ALL SDKs work with your application code:**

```python
# Your business logic stays the same!
def checkout(gateway: PaymentGateway, amount: float):
    result = gateway.process_payment(amount)
    if result["success"]:
        print(f"✅ Payment successful: {result['transaction_id']}")
    return result


# Now they ALL work! ✅
stripe_gateway = StripeAdapter("sk_test_123")
checkout(stripe_gateway, 100.00)  # ✅ Works!

paypal_gateway = PayPalAdapter("client_123", "secret_456")
checkout(paypal_gateway, 100.00)  # ✅ Works!

square_gateway = SquareAdapter("api_key_789")
checkout(square_gateway, 100.00)  # ✅ Works!


# Your application code doesn't care which one!
def process_order(payment_method: str, amount: float):
    if payment_method == "stripe":
        gateway = StripeAdapter("sk_test_123")
    elif payment_method == "paypal":
        gateway = PayPalAdapter("client_123", "secret_456")
    elif payment_method == "square":
        gateway = SquareAdapter("api_key_789")
    
    return checkout(gateway, amount)  # Same interface for all!
```

---

## 🏗️ Implementation Patterns

### Pattern 1: Object Adapter (Composition) ⭐ Recommended

```python
class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee  # Composition
    
    def request(self):
        # Translate Target.request() → Adaptee.specific_request()
        return self.adaptee.specific_request()
```

**Example:**

```python
# Target interface (what client expects)
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str):
        pass

# Adaptee (incompatible interface)
class VLCPlayer:
    def play_vlc(self, filename: str):
        print(f"Playing {filename} with VLC")

# Adapter (uses composition)
class VLCAdapter(MediaPlayer):
    def __init__(self):
        self.vlc_player = VLCPlayer()  # Composition
    
    def play(self, filename: str):
        # Translate play() → play_vlc()
        self.vlc_player.play_vlc(filename)

# Usage
player: MediaPlayer = VLCAdapter()
player.play("movie.mp4")  # Works!
```

### Pattern 2: Class Adapter (Multiple Inheritance)

```python
class Adapter(Target, Adaptee):
    def request(self):
        # Translate using inherited method
        return self.specific_request()
```

**Example:**

```python
# Target interface
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str):
        pass

# Adaptee
class VLCPlayer:
    def play_vlc(self, filename: str):
        print(f"Playing {filename} with VLC")

# Class Adapter (multiple inheritance)
class VLCAdapter(MediaPlayer, VLCPlayer):
    def play(self, filename: str):
        # Call inherited method from VLCPlayer
        self.play_vlc(filename)

# Usage
player: MediaPlayer = VLCAdapter()
player.play("movie.mp4")
```

**Object Adapter vs Class Adapter:**

| Aspect | Object Adapter | Class Adapter |
|--------|---------------|---------------|
| **Technique** | Composition | Multiple Inheritance |
| **Flexibility** | Can adapt entire hierarchy | Adapts specific class only |
| **Python** | ✅ Recommended | Less common |
| **Advantage** | More flexible, loose coupling | Can override adaptee methods |

---

## 💳 Real-World Example: Complete Payment Gateway System

### Complete Implementation

```python
from abc import ABC, abstractmethod
from typing import Dict

# Step 1: Third-Party SDKs (can't modify these!)

class StripeSDK:
    """Third-party Stripe SDK"""
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def create_charge(self, amount_cents: int, currency: str = "usd") -> object:
        class StripeCharge:
            def __init__(self, amount):
                self.id = f"ch_{amount}"
                self.paid = True
                self.amount = amount
        return StripeCharge(amount_cents)


class PayPalSDK:
    """Third-party PayPal SDK"""
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def execute_payment(self, payment_data: dict) -> object:
        class PayPalPayment:
            def __init__(self, data):
                self.state = "approved"
                self.payment_id = f"PAY-{data['amount']}"
        return PayPalPayment(payment_data)


class SquareSDK:
    """Third-party Square SDK"""
    def __init__(self, access_token: str, location_id: str):
        self.access_token = access_token
        self.location_id = location_id
    
    def create_payment(self, amount_money: Dict, source_id: str) -> object:
        class SquarePayment:
            def __init__(self, amount, currency):
                self.id = f"square_{amount}"
                self.status = "COMPLETED"
                self.amount_money = {"amount": amount, "currency": currency}
        return SquarePayment(amount_money["amount"], amount_money["currency"])


class RazorpaySDK:
    """Third-party Razorpay SDK (uses paise - 1 rupee = 100 paise)"""
    def __init__(self, key_id: str, key_secret: str):
        self.key_id = key_id
        self.key_secret = key_secret
    
    def payment_capture(self, payment_id: str, amount_paise: int) -> Dict:
        return {
            "id": payment_id,
            "entity": "payment",
            "amount": amount_paise,
            "currency": "INR",
            "status": "captured"
        }


# Step 2: Target Interface (YOUR application's interface)

class PaymentGateway(ABC):
    """Standard payment interface for YOUR application"""
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str = "USD") -> Dict:
        """
        Process a payment.
        
        Args:
            amount: Amount in dollars/rupees (depending on currency)
            currency: Currency code (default: USD)
        
        Returns:
            dict with keys: success (bool), transaction_id (str), message (str)
        """
        pass


# Step 3: Adapters (translate SDKs to YOUR interface)

class StripeAdapter(PaymentGateway):
    """Adapter to make Stripe SDK work with PaymentGateway interface"""
    
    def __init__(self, secret_key: str):
        self.stripe_sdk = StripeSDK(secret_key)
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict:
        """Adapt PaymentGateway interface to Stripe SDK"""
        
        # Translate dollars to cents
        amount_in_cents = int(amount * 100)
        
        try:
            # Call Stripe SDK
            charge = self.stripe_sdk.create_charge(amount_in_cents, currency.lower())
            
            # Translate Stripe response to standard format
            return {
                "success": charge.paid,
                "transaction_id": charge.id,
                "message": "Payment processed via Stripe"
            }
        except Exception as e:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"Stripe payment failed: {str(e)}"
            }


class PayPalAdapter(PaymentGateway):
    """Adapter for PayPal SDK"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.paypal_sdk = PayPalSDK(client_id, client_secret)
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict:
        """Adapt PaymentGateway interface to PayPal SDK"""
        
        # Prepare PayPal SDK request format
        payment_data = {
            "amount": amount,
            "currency": currency
        }
        
        try:
            # Call PayPal SDK
            payment = self.paypal_sdk.execute_payment(payment_data)
            
            # Translate PayPal response to standard format
            return {
                "success": payment.state == "approved",
                "transaction_id": payment.payment_id,
                "message": "Payment processed via PayPal"
            }
        except Exception as e:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"PayPal payment failed: {str(e)}"
            }


class SquareAdapter(PaymentGateway):
    """Adapter for Square SDK"""
    
    def __init__(self, access_token: str, location_id: str):
        self.square_sdk = SquareSDK(access_token, location_id)
        self.location_id = location_id
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict:
        """Adapt PaymentGateway interface to Square SDK"""
        
        # Translate dollars to cents
        amount_in_cents = int(amount * 100)
        
        # Prepare Square SDK request format
        amount_money = {
            "amount": amount_in_cents,
            "currency": currency
        }
        
        # Get payment source (simplified - normally from customer)
        source_id = "default_card_source"
        
        try:
            # Call Square SDK
            payment = self.square_sdk.create_payment(amount_money, source_id)
            
            # Translate Square response to standard format
            return {
                "success": payment.status == "COMPLETED",
                "transaction_id": payment.id,
                "message": "Payment processed via Square"
            }
        except Exception as e:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"Square payment failed: {str(e)}"
            }


class RazorpayAdapter(PaymentGateway):
    """Adapter for Razorpay SDK"""
    
    def __init__(self, key_id: str, key_secret: str):
        self.razorpay_sdk = RazorpaySDK(key_id, key_secret)
    
    def process_payment(self, amount: float, currency: str = "USD") -> Dict:
        """Adapt PaymentGateway interface to Razorpay SDK"""
        
        # Convert to INR if needed (simplified)
        if currency == "USD":
            amount_inr = amount * 83  # USD to INR conversion
        else:
            amount_inr = amount
        
        # Convert to paise (Razorpay uses paise)
        amount_paise = int(amount_inr * 100)
        
        # Generate payment ID (simplified)
        payment_id = f"pay_{amount_paise}"
        
        try:
            # Call Razorpay SDK
            response = self.razorpay_sdk.payment_capture(payment_id, amount_paise)
            
            # Translate to standard format
            return {
                "success": response["status"] == "captured",
                "transaction_id": response["id"],
                "message": "Payment processed via Razorpay"
            }
        except Exception as e:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"Razorpay payment failed: {str(e)}"
            }


# Step 4: Business Logic (unchanged, works with ALL adapters!)

class PaymentProcessor:
    """Business logic - works with ANY payment gateway"""
    
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    
    def checkout(self, amount: float) -> bool:
        """Process checkout - works with ANY gateway!"""
        print(f"\nProcessing payment of ${amount}...")
        
        result = self.gateway.process_payment(amount)
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Transaction ID: {result['transaction_id']}")
            return True
        else:
            print(f"❌ {result['message']}")
            return False


# Step 5: Usage - All gateways work the same way!

def main():
    # Create adapters for third-party SDKs
    stripe = StripeAdapter("sk_test_123")
    paypal = PayPalAdapter("paypal_client_id", "paypal_secret")
    square = SquareAdapter("square_token", "location_123")
    razorpay = RazorpayAdapter("rzp_key", "rzp_secret")
    
    # All work with same interface!
    processor = PaymentProcessor(stripe)
    processor.checkout(100.00)
    
    processor = PaymentProcessor(paypal)
    processor.checkout(150.00)
    
    processor = PaymentProcessor(square)
    processor.checkout(200.00)
    
    processor = PaymentProcessor(razorpay)
    processor.checkout(250.00)
    
    # Easy to switch payment providers!
    def process_order(payment_method: str, amount: float):
        gateways = {
            "stripe": StripeAdapter("sk_test_123"),
            "paypal": PayPalAdapter("client_id", "secret"),
            "square": SquareAdapter("token", "location"),
            "razorpay": RazorpayAdapter("key", "secret")
        }
        
        gateway = gateways.get(payment_method)
        if gateway:
            processor = PaymentProcessor(gateway)
            return processor.checkout(amount)
        else:
            print(f"Unknown payment method: {payment_method}")
            return False


if __name__ == "__main__":
    main()
```

---

## 🎨 Adapter Pattern Structure

```
┌─────────────────┐
│     Client      │  (Your business logic)
└────────┬────────┘
         │ uses
         ↓
┌─────────────────┐
│     Target      │  (Expected interface: PaymentGateway)
│   <<interface>> │
│   + process_    │
│     payment()   │
└────────┬────────┘
         ↑ implements
         │
    ┌────┴────────────────┐
    │                     │
┌───────────┐  ┌──────────────────┐
│ Original  │  │     Adapter      │  (StripeAdapter, PayPalAdapter)
│ Concrete  │  │                  │
│ Classes   │  │  - third_party_  │  (Contains incompatible SDK)
└───────────┘  │    sdk           │
               │  + process_      │  (Implements target interface)
               │    payment()     │  (Translates calls)
               └────────┬─────────┘
                        │ delegates to
                        ↓
               ┌────────────────────┐
               │      Adaptee       │  (StripeSDK, PayPalSDK)
               │                    │
               │  + create_charge() │  (Incompatible interface)
               │  + execute_       │
               │    payment()       │
               └────────────────────┘
```

---

## 📱 More Real-World Examples

### Example 1: Legacy Logger Adapter

```python
# Modern interface
class Logger(ABC):
    @abstractmethod
    def log(self, level: str, message: str, **kwargs):
        pass

# Legacy system
class LegacyLogger:
    def write_to_file(self, text: str):
        with open("legacy.log", "a") as f:
            f.write(text + "\n")

# Adapter
class LegacyLoggerAdapter(Logger):
    def __init__(self):
        self.legacy_logger = LegacyLogger()
    
    def log(self, level: str, message: str, **kwargs):
        # Format for legacy system
        formatted = f"[{level}] {message}"
        if kwargs:
            formatted += f" | {kwargs}"
        
        # Translate to legacy interface
        self.legacy_logger.write_to_file(formatted)

# Usage
logger: Logger = LegacyLoggerAdapter()
logger.log("INFO", "Application started", user="admin")
```

### Example 2: Data Format Adapter

```python
# Modern API expects JSON
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: dict) -> dict:
        pass

# Legacy system returns XML
class LegacyXMLService:
    def get_data(self) -> str:
        return "<user><name>Alice</name><age>25</age></user>"

# Adapter
import xml.etree.ElementTree as ET

class XMLToJSONAdapter(DataProcessor):
    def __init__(self):
        self.xml_service = LegacyXMLService()
    
    def process(self, data: dict = None) -> dict:
        # Get XML from legacy service
        xml_data = self.xml_service.get_data()
        
        # Convert XML to dict
        root = ET.fromstring(xml_data)
        result = {
            "name": root.find("name").text,
            "age": int(root.find("age").text)
        }
        
        return result

# Usage
processor: DataProcessor = XMLToJSONAdapter()
user_data = processor.process()
print(user_data)  # {"name": "Alice", "age": 25}
```

### Example 3: Third-Party Email Service Adapter

```python
# Your interface
class EmailSender(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str):
        pass

# Third-party library (e.g., SendGrid)
class SendGridAPI:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def send_email(self, email_data: dict):
        # SendGrid's format
        print(f"Sending via SendGrid: {email_data}")

# Adapter
class SendGridAdapter(EmailSender):
    def __init__(self, api_key: str):
        self.sendgrid = SendGridAPI(api_key)
    
    def send(self, to: str, subject: str, body: str):
        # Translate to SendGrid format
        email_data = {
            "personalizations": [{
                "to": [{"email": to}]
            }],
            "from": {"email": "noreply@example.com"},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}]
        }
        
        # Use SendGrid API
        self.sendgrid.send_email(email_data)

# Usage
sender: EmailSender = SendGridAdapter("sendgrid_api_key")
sender.send("user@example.com", "Hello", "Welcome!")
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Over-Adapting

```python
# ❌ Don't create adapters for everything
class SimpleCalculator:
    def add(self, a, b):
        return a + b

# Unnecessary adapter!
class CalculatorAdapter:
    def __init__(self):
        self.calc = SimpleCalculator()
    
    def add(self, a, b):
        return self.calc.add(a, b)  # Just delegating - no adaptation!

# ✅ Use adapter only when interfaces are incompatible
```

### Pitfall 2: Losing Type Information

```python
# ❌ Generic adapter loses type info
class GenericAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def call(self, method, *args):
        return getattr(self.adaptee, method)(*args)

# Hard to use, no IDE support
adapter = GenericAdapter(some_object)
result = adapter.call("some_method", arg1, arg2)  # What does this do?

# ✅ Specific adapter with clear interface
class SpecificAdapter(TargetInterface):
    def __init__(self, adaptee: SpecificType):
        self.adaptee = adaptee
    
    def target_method(self, param: str) -> int:
        # Clear transformation
        return self.adaptee.specific_method(param)
```

### Pitfall 3: Not Handling Errors

```python
# ❌ No error handling
class PaymentAdapter(PaymentGateway):
    def process_payment(self, amount: float) -> dict:
        response = self.third_party_sdk.charge(amount * 100)
        return {"success": True, "id": response.id}  # What if it fails?

# ✅ Proper error handling
class PaymentAdapter(PaymentGateway):
    def process_payment(self, amount: float) -> dict:
        try:
            response = self.third_party_sdk.charge(amount * 100)
            return {
                "success": response.status == "SUCCESS",
                "id": response.id
            }
        except ThirdPartyException as e:
            return {
                "success": False,
                "id": None,
                "error": str(e)
            }
```

---

## 💡 Best Practices

### 1. Keep Adapters Simple

```python
# ✅ Simple, focused adapter
class SquareAdapter(PaymentGateway):
    def __init__(self, sdk):
        self.sdk = sdk
    
    def process_payment(self, amount):
        # Just translation, no business logic
        cents = amount * 100
        response = self.sdk.charge(cents)
        return self._convert_response(response)
```

### 2. Document Adaptations

```python
class SquareAdapter(PaymentGateway):
    """
    Adapter for Square SDK.
    
    Translations:
    - process_payment(amount) → square_sdk.charge_card(amount * 100, token)
    - Converts dollars to cents
    - Maps SquareResponse.status == "SUCCESS" → {"success": True}
    - Extracts transaction_id from SquareResponse.transaction_id
    """
    pass
```

### 3. Test Adapters Thoroughly

```python
def test_square_adapter():
    # Test parameter conversion
    adapter = SquareAdapter("key")
    result = adapter.process_payment(100.00)
    # Verify cents conversion happened
    assert adapter.last_call_amount == 10000
    
    # Test response conversion
    assert "success" in result
    assert "transaction_id" in result
```

---

## 🎯 When to Use Adapter Pattern

### ✅ Use Adapter When:

1. **Third-party library integration**
   - Library has incompatible interface
   - Can't modify library code
   - Want to isolate external dependencies

2. **Legacy code integration**
   - Old system with different interface
   - Can't rewrite legacy code
   - Need gradual migration

3. **Multiple incompatible interfaces**
   - Different vendors/libraries for same functionality (Stripe, PayPal, Square)
   - Want unified interface for all

4. **Interface evolution**
   - Old interface must coexist with new
   - Gradual migration needed

### ❌ Don't Use When:

1. **Simple delegation**
   - No actual interface incompatibility
   - Just forwarding calls

2. **Can modify the source**
   - Prefer direct implementation
   - Adapter adds unnecessary complexity

3. **Performance critical**
   - Extra layer adds overhead
   - Direct integration better

---

## 🔑 Key Takeaways

- **What:** Wrapper that makes incompatible interfaces work together
- **Why:** Integrate third-party/legacy code without modification
- **When:** Interface incompatibility, can't change source code
- **How:** Implement target interface, wrap incompatible object, translate calls

**Remember:**
- Adapter = Interface translator
- Use composition (Object Adapter) in Python
- Keep adapters simple and focused
- Document what's being adapted
- Test thoroughly
- Each third-party SDK needs its own adapter

**Adapter vs Other Patterns:**
- **Facade:** Simplifies complex interface (makes it easier)
- **Decorator:** Adds behavior, keeps same interface
- **Adapter:** Changes interface to make it compatible

**Real-World Use Case:**
In payment systems, Stripe, PayPal, and Square are ALL third-party SDKs with completely different interfaces. The Adapter Pattern lets you create a **unified interface** (PaymentGateway) for your application while using their native SDKs under the hood. This makes it easy to:
- Switch between payment providers
- Add new payment providers
- Keep your business logic clean and consistent

The Adapter Pattern is about **making incompatible things work together**! 🔌