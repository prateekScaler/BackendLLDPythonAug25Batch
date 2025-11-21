"""
Adapter Design Pattern - Demo
Practical examples showing how to integrate incompatible interfaces.
"""

from abc import ABC, abstractmethod
from typing import Dict

# ============================================================================
# Example 1: Payment Gateway Integration
# ============================================================================

print("=" * 70)
print("Example 1: Payment Gateway Integration - The Core Problem")
print("=" * 70)

# Your existing payment system interface
class PaymentGateway(ABC):
    """Standard payment gateway interface your system expects"""
    
    @abstractmethod
    def process_payment(self, amount: float) -> Dict:
        """
        Process a payment.
        Returns: {"success": bool, "transaction_id": str, "message": str}
        """
        pass


# Your existing implementations
class StripeGateway(PaymentGateway):
    """Stripe implementation - matches your interface"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def process_payment(self, amount: float) -> Dict:
        # Stripe implementation
        return {
            "success": True,
            "transaction_id": f"stripe_{int(amount*100)}",
            "message": "Processed via Stripe"
        }


class PayPalGateway(PaymentGateway):
    """PayPal implementation - matches your interface"""
    
    def __init__(self, client_id: str):
        self.client_id = client_id
    
    def process_payment(self, amount: float) -> Dict:
        # PayPal implementation
        return {
            "success": True,
            "transaction_id": f"paypal_{int(amount*100)}",
            "message": "Processed via PayPal"
        }


# Third-party Square SDK (incompatible interface!)
class SquareSDK:
    """Square SDK - can't modify this third-party code!"""
    
    def __init__(self, access_token: str, location_id: str):
        self.access_token = access_token
        self.location_id = location_id
    
    def create_payment(self, amount_cents: int, currency: str) -> 'SquarePayment':
        """
        Different interface!
        - Takes cents instead of dollars
        - Returns SquarePayment object instead of dict
        """
        return SquarePayment(
            payment_id=f"square_{amount_cents}",
            status="COMPLETED",
            amount_cents=amount_cents
        )


class SquarePayment:
    """Square's payment response object"""
    
    def __init__(self, payment_id: str, status: str, amount_cents: int):
        self.payment_id = payment_id
        self.status = status
        self.amount_cents = amount_cents


# ❌ Problem: Can't use Square SDK directly!
print("\n❌ Problem Demonstration:")
print("-" * 70)

square_sdk = SquareSDK("token_xyz", "loc_123")

# This doesn't work!
print("Trying to use Square SDK directly...")
print("square_sdk.process_payment(100.00)  # ❌ No such method!")
print("square_sdk.create_payment(100.00, 'USD')  # ❌ Wrong parameters!")

# ✅ Solution: Create an Adapter!
print("\n✅ Solution: Adapter Pattern")
print("-" * 70)


class SquareAdapter(PaymentGateway):
    """Adapter to make Square SDK work with PaymentGateway interface"""
    
    def __init__(self, access_token: str, location_id: str):
        self.square_sdk = SquareSDK(access_token, location_id)
    
    def process_payment(self, amount: float) -> Dict:
        """Implement PaymentGateway interface, translate to Square SDK"""
        
        # 1. Convert dollars to cents
        amount_cents = int(amount * 100)
        
        # 2. Call Square SDK with its interface
        payment = self.square_sdk.create_payment(amount_cents, "USD")
        
        # 3. Convert Square response to expected dict format
        return {
            "success": payment.status == "COMPLETED",
            "transaction_id": payment.payment_id,
            "message": "Processed via Square"
        }


# Now Square works with your system!
square_gateway = SquareAdapter("token_xyz", "loc_123")

# Your business logic (unchanged!)
def checkout(gateway: PaymentGateway, amount: float):
    """Business logic - works with ANY PaymentGateway"""
    print(f"\nProcessing ${amount} payment...")
    result = gateway.process_payment(amount)
    
    if result["success"]:
        print(f"  ✅ {result['message']}")
        print(f"  Transaction ID: {result['transaction_id']}")
    else:
        print(f"  ❌ Failed: {result['message']}")
    
    return result


print("\nTesting all gateways with same interface:")
checkout(StripeGateway("stripe_key"), 100.00)
checkout(PayPalGateway("paypal_id"), 150.00)
checkout(SquareAdapter("square_token", "loc_123"), 200.00)  # Works now!

# ============================================================================
# Example 2: Multiple Third-Party Adapters
# ============================================================================

print("\n" + "=" * 70)
print("Example 2: Multiple Third-Party SDKs - Razorpay Integration")
print("=" * 70)

# Another third-party SDK with different interface
class RazorpaySDK:
    """Razorpay SDK - different interface and currency (INR, paise)"""
    
    def __init__(self, key_id: str, key_secret: str):
        self.key_id = key_id
        self.key_secret = key_secret
    
    def capture_payment(self, payment_id: str, amount_paise: int) -> Dict:
        """
        Razorpay uses paise (100 paise = 1 rupee)
        Returns different format again!
        """
        return {
            "id": payment_id,
            "amount": amount_paise,
            "currency": "INR",
            "status": "captured"
        }


class RazorpayAdapter(PaymentGateway):
    """Adapter for Razorpay SDK"""
    
    def __init__(self, key_id: str, key_secret: str):
        self.razorpay_sdk = RazorpaySDK(key_id, key_secret)
        self.usd_to_inr_rate = 83.0  # Simplified exchange rate
    
    def process_payment(self, amount: float) -> Dict:
        """Adapt PaymentGateway interface to Razorpay SDK"""
        
        # 1. Convert USD to INR
        amount_inr = amount * self.usd_to_inr_rate
        
        # 2. Convert to paise
        amount_paise = int(amount_inr * 100)
        
        # 3. Generate payment ID
        payment_id = f"pay_{amount_paise}"
        
        # 4. Call Razorpay SDK
        response = self.razorpay_sdk.capture_payment(payment_id, amount_paise)
        
        # 5. Translate to standard format
        return {
            "success": response["status"] == "captured",
            "transaction_id": response["id"],
            "message": f"Processed via Razorpay ({amount_inr:.2f} INR)"
        }


print("\nTesting Razorpay adapter:")
razorpay = RazorpayAdapter("rzp_key", "rzp_secret")
checkout(razorpay, 10.00)

# ============================================================================
# Example 3: Legacy System Integration
# ============================================================================

print("\n" + "=" * 70)
print("Example 3: Legacy System Integration")
print("=" * 70)

# Legacy payment system (old interface, can't modify)
class LegacyPaymentProcessor:
    """Old payment system - different interface"""
    
    def charge_customer(self, customer_id: int, dollars: float, cents: int) -> int:
        """
        Legacy interface - weird parameters!
        - Splits dollars and cents
        - Returns 0 for success, error code otherwise
        """
        total_cents = int(dollars * 100) + cents
        print(f"  [LEGACY] Charging customer #{customer_id}: ${dollars}.{cents:02d}")
        return 0  # Success


# Adapter for legacy system
class LegacyPaymentAdapter(PaymentGateway):
    """Adapter to use legacy system with modern interface"""
    
    def __init__(self, customer_id: int):
        self.legacy_system = LegacyPaymentProcessor()
        self.customer_id = customer_id
    
    def process_payment(self, amount: float) -> Dict:
        """Translate modern interface to legacy interface"""
        
        # 1. Split amount into dollars and cents
        dollars = int(amount)
        cents = int((amount - dollars) * 100)
        
        # 2. Call legacy system
        result_code = self.legacy_system.charge_customer(
            self.customer_id, dollars, cents
        )
        
        # 3. Translate result code to dict
        return {
            "success": result_code == 0,
            "transaction_id": f"legacy_{self.customer_id}_{int(amount*100)}",
            "message": "Processed via Legacy System"
        }


print("\nTesting legacy system adapter:")
legacy = LegacyPaymentAdapter(customer_id=12345)
checkout(legacy, 99.99)

# ============================================================================
# Example 4: Payment Gateway Factory with Adapters
# ============================================================================

print("\n" + "=" * 70)
print("Example 4: Factory Pattern + Adapter Pattern")
print("=" * 70)


class PaymentGatewayFactory:
    """Factory to create payment gateways (mix of native and adapted)"""
    
    @staticmethod
    def create(gateway_type: str) -> PaymentGateway:
        """Create payment gateway by type"""
        
        if gateway_type == "stripe":
            return StripeGateway("stripe_api_key")
        
        elif gateway_type == "paypal":
            return PayPalGateway("paypal_client_id")
        
        elif gateway_type == "square":
            # Adapted third-party SDK
            return SquareAdapter("square_token", "location_123")
        
        elif gateway_type == "razorpay":
            # Adapted third-party SDK
            return RazorpayAdapter("rzp_key", "rzp_secret")
        
        elif gateway_type == "legacy":
            # Adapted legacy system
            return LegacyPaymentAdapter(customer_id=99999)
        
        else:
            raise ValueError(f"Unknown gateway type: {gateway_type}")


print("\nUsing factory to create all gateways:")
gateway_types = ["stripe", "paypal", "square", "razorpay", "legacy"]

for gw_type in gateway_types:
    gateway = PaymentGatewayFactory.create(gw_type)
    checkout(gateway, 50.00)

# ============================================================================
# Example 5: Two-Way Adapter (Bonus)
# ============================================================================

print("\n" + "=" * 70)
print("Example 5: Two-Way Adapter (Advanced)")
print("=" * 70)


class ModernAPI(ABC):
    """Modern API interface"""
    
    @abstractmethod
    def send_request(self, data: Dict) -> Dict:
        pass


class LegacyAPI:
    """Legacy API with different interface"""
    
    def process(self, xml_data: str) -> str:
        return f"<response>Success: {xml_data}</response>"


class TwoWayAdapter(ModernAPI, LegacyAPI):
    """Adapter that works both ways!"""
    
    def __init__(self):
        self.legacy_api = LegacyAPI()
    
    # Modern → Legacy
    def send_request(self, data: Dict) -> Dict:
        """Modern interface implementation"""
        # Convert dict to XML
        xml = f"<request>{data}</request>"
        
        # Call legacy
        xml_response = self.legacy_api.process(xml)
        
        # Convert XML back to dict
        return {"result": xml_response}
    
    # Legacy → Modern (if needed)
    def process(self, xml_data: str) -> str:
        """Legacy interface implementation"""
        # Could convert to dict and call modern API
        return super().process(xml_data)


adapter = TwoWayAdapter()
result = adapter.send_request({"action": "payment", "amount": 100})
print(f"\nTwo-way adapter result: {result}")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 70)
print("Summary: Adapter Pattern Benefits")
print("=" * 70)
print("""
✅ Adapter Pattern Solved:
  1. Integrated Square SDK (different method names, parameters, return type)
  2. Integrated Razorpay SDK (different currency, units)
  3. Integrated legacy system (old interface)
  4. All work with same business logic (checkout function)
  5. No modification to existing code!

🔑 Key Points:
  - Adapter implements target interface (PaymentGateway)
  - Adapter wraps incompatible object (SquareSDK, etc.)
  - Adapter translates calls between interfaces
  - Use Object Adapter (composition) in Python

⚡ When to Use:
  - Third-party library integration
  - Legacy code integration
  - Multiple incompatible interfaces for same functionality
  - Can't modify the incompatible code

🎯 Result:
  Your code works with ANY payment gateway through a single interface,
  whether it's your own implementation or a third-party SDK!
""")
