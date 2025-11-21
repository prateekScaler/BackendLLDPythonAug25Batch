# Understanding SDKs and Why Adapter Pattern Needs Them

## 🤔 What is an SDK?

**SDK = Software Development Kit**

Think of an SDK as a **toolbox provided by a company** that lets you use their service in your code.

### Real-World Analogy

Imagine you want to accept payments in your online store:

**Without SDK:**
```python
# You'd have to do THIS manually:
import requests
import json
import hmac
import hashlib

# Manually construct HTTP request
headers = {
    "Authorization": "Bearer sk_test_xyz123",
    "Content-Type": "application/json"
}

data = {
    "amount": 10000,  # Wait, is this dollars or cents?
    "currency": "usd",
    "source": "tok_visa",
    "description": "Order #123"
}

# Manually sign the request
signature = hmac.new(
    secret_key.encode(),
    json.dumps(data).encode(),
    hashlib.sha256
).hexdigest()

# Make HTTP request
response = requests.post(
    "https://api.stripe.com/v1/charges",
    headers=headers,
    json=data
)

# Parse response manually
if response.status_code == 200:
    result = response.json()
    # Now what? What fields exist?
    # What does success look like?
```

**With SDK (Stripe SDK):**
```python
import stripe

stripe.api_key = "sk_test_xyz123"

# SDK handles everything!
charge = stripe.Charge.create(
    amount=10000,
    currency="usd",
    source="tok_visa",
    description="Order #123"
)

# SDK gives you a nice object
print(charge.id)
print(charge.status)
```

---

## 📦 What Does an SDK Contain?

An SDK typically includes:

1. **Pre-written Code (Library)**
   ```python
   # Stripe SDK provides classes like:
   stripe.Charge
   stripe.Customer
   stripe.PaymentIntent
   ```

2. **Authentication Handling**
   ```python
   # SDK handles API keys, OAuth, tokens
   stripe.api_key = "your_key"  # That's it!
   ```

3. **Error Handling**
   ```python
   # SDK provides specific error types
   try:
       charge = stripe.Charge.create(...)
   except stripe.error.CardError as e:
       print("Card was declined")
   except stripe.error.RateLimitError as e:
       print("Too many requests")
   ```

4. **Data Models**
   ```python
   # SDK provides typed objects
   charge.id           # Auto-completion works!
   charge.amount
   charge.created
   ```

5. **Documentation**
   - How to install
   - How to use
   - Examples

---

## 🌍 Real-World SDK Examples

### Example 1: Payment SDKs

```python
# Stripe SDK
import stripe
stripe.Charge.create(amount=1000, currency="usd")

# PayPal SDK
import paypalrestsdk
paypalrestsdk.Payment.create({...})

# Square SDK
from square.client import Client
client = Client(access_token="...")
client.payments.create_payment({...})
```

**Each company provides their OWN SDK with DIFFERENT interfaces!**

### Example 2: Cloud Storage SDKs

```python
# AWS S3 SDK
import boto3
s3 = boto3.client('s3')
s3.upload_file('file.txt', 'bucket', 'key')

# Google Cloud Storage SDK
from google.cloud import storage
client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('file.txt')
blob.upload_from_filename('file.txt')

# Azure Blob Storage SDK
from azure.storage.blob import BlobServiceClient
blob_service = BlobServiceClient(...)
blob_client = blob_service.get_blob_client(...)
blob_client.upload_blob(data)
```

**Different companies = Different SDKs = Different interfaces!**

### Example 3: Email SDKs

```python
# SendGrid SDK
import sendgrid
sg = sendgrid.SendGridAPIClient(api_key)
sg.send(message)

# Mailgun SDK
import mailgun
mailgun.send_email(to, subject, body)

# Amazon SES SDK
import boto3
ses = boto3.client('ses')
ses.send_email(Source, Destination, Message)
```

---

## 🎯 Why Do SDKs Have Different Interfaces?

### Reason 1: Company Design Choices

Each company designs their SDK based on:
- Their internal architecture
- Their API structure
- Their language preferences
- Their design philosophy

```python
# Stripe likes objects and methods
charge = stripe.Charge.create(...)

# PayPal likes dictionaries and functions
payment = paypalrestsdk.Payment.create({...})

# Square likes builder patterns
payment = (
    CreatePaymentRequest.Builder()
    .amount_money(...)
    .source_id(...)
    .build()
)
```

### Reason 2: Different Domain Requirements

```python
# Stripe: Simple online payments
stripe.Charge.create(amount=1000)

# Square: Point-of-sale systems
square.create_payment(
    amount_money={...},
    location_id="...",    # Physical location needed!
    customer_id="..."     # In-person customer
)

# PayPal: Digital wallet focus
paypal.execute_payment(
    payment_id="...",     # Two-step process
    payer_id="..."        # PayPal account required
)
```

### Reason 3: Evolution Over Time

```python
# Old Stripe API (v1)
stripe.Charge.create(...)

# New Stripe API (v2)
stripe.PaymentIntent.create(...)  # Different object!

# Your code might use both if you have legacy systems
```

---

## 🏚️ What Are Legacy Systems?

**Legacy System = Old code that still works but uses outdated technology**

### Characteristics:

1. **Old Technology**
   ```python
   # Legacy system from 2005
   class OldPaymentSystem:
       def process_credit_card(self, card_number, amount):
           # Uses outdated methods
           # No encryption
           # No modern security
           pass
   ```

2. **Can't Easily Change**
   ```python
   # Why you can't change legacy code:
   # - No original developers
   # - No documentation
   # - Too risky to modify (might break production)
   # - Other systems depend on it
   # - Would cost millions to rewrite
   ```

3. **Different Interface**
   ```python
   # Modern system
   def process_payment(amount: float, currency: str) -> dict:
       return {"success": True, "id": "txn_123"}
   
   # Legacy system
   def ExecuteTransaction(amt, curr_code):
       return "SUCCESS:TXN123"  # Different format!
   ```

### Real-World Legacy Example

```python
# Imagine a bank's core system from 1980s
# Written in COBOL, wrapped in Python

class LegacyBankingSystem:
    """
    This system processes $10 billion daily.
    It CANNOT be turned off or rewritten.
    It's been running for 40 years!
    """
    
    def EXEC_TXN(self, acct_num, amt_cents, txn_type):
        """
        Parameters:
        - acct_num: 16-digit string
        - amt_cents: integer (no decimals!)
        - txn_type: "D" for debit, "C" for credit
        
        Returns:
        - Status code: "00" = success, others = error codes
        - Transaction ID: 20-character string
        """
        # This talks to a mainframe computer!
        return ("00", "TXN20231115000001234")
```

**You MUST use this system, but your modern app needs a clean interface!**

---

## 🔗 Why Adapter Pattern is Essential for SDKs

### Problem: Multiple SDKs in One Application

Imagine you're building an e-commerce platform:

```python
# Your application needs to:
# 1. Accept payments (Stripe, PayPal, Square)
# 2. Send emails (SendGrid, Mailgun)
# 3. Store files (AWS S3, Google Cloud, Azure)
# 4. Send SMS (Twilio, Nexmo)

# Without Adapter Pattern - NIGHTMARE!

def process_order(order):
    # Payment processing - different for each!
    if order.payment_method == "stripe":
        charge = stripe.Charge.create(
            amount=int(order.amount * 100),
            currency="usd"
        )
        success = charge.paid
        txn_id = charge.id
    
    elif order.payment_method == "paypal":
        payment = paypalrestsdk.Payment.create({
            "amount": {"total": str(order.amount), "currency": "USD"}
        })
        success = payment.state == "approved"
        txn_id = payment.id
    
    elif order.payment_method == "square":
        payment = square_client.payments.create_payment(
            body={
                "amount_money": {
                    "amount": int(order.amount * 100),
                    "currency": "USD"
                }
            }
        )
        success = payment.payment.status == "COMPLETED"
        txn_id = payment.payment.id
    
    # This is unmaintainable!
    # What if you add more payment methods?
    # What if an SDK changes?
```

### Solution: Adapter Pattern

```python
# With Adapter Pattern - CLEAN!

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        pass

class StripeAdapter(PaymentGateway):
    def process_payment(self, amount: float) -> dict:
        charge = stripe.Charge.create(amount=int(amount * 100))
        return {"success": charge.paid, "transaction_id": charge.id}

class PayPalAdapter(PaymentGateway):
    def process_payment(self, amount: float) -> dict:
        payment = paypalrestsdk.Payment.create({"amount": {"total": str(amount)}})
        return {"success": payment.state == "approved", "transaction_id": payment.id}

class SquareAdapter(PaymentGateway):
    def process_payment(self, amount: float) -> dict:
        payment = square_client.payments.create_payment(...)
        return {"success": payment.payment.status == "COMPLETED", "transaction_id": payment.payment.id}

# Now your business logic is simple!
def process_order(order, payment_gateway: PaymentGateway):
    result = payment_gateway.process_payment(order.amount)
    
    if result["success"]:
        save_transaction(result["transaction_id"])
        send_confirmation_email(order)
    else:
        notify_customer_payment_failed(order)

# Easy to switch payment providers!
gateway = get_payment_gateway(order.payment_method)
process_order(order, gateway)
```

---

## 📊 Why Companies Use Multiple SDKs

### Reason 1: Business Requirements

```python
# E-commerce platform needs:

# Multiple payment processors (for redundancy)
if stripe_down:
    use_paypal_gateway()

# Regional requirements
if customer.country == "India":
    use_razorpay()  # Popular in India
elif customer.country == "USA":
    use_stripe()    # Popular in USA

# Customer preference
if customer.preferred_method == "paypal":
    use_paypal()
```

### Reason 2: Cost Optimization

```python
# Different SDKs have different fees

# Stripe: 2.9% + $0.30 per transaction
# PayPal: 2.9% + $0.30 per transaction
# Square: 2.6% + $0.10 per transaction (for in-person)

# Route to cheapest option
if transaction_amount > 100:
    use_square()  # Better for large amounts
else:
    use_stripe()  # Better integration
```

### Reason 3: Feature Requirements

```python
# Different SDKs have different features

# Need subscriptions? Stripe is best
if order.is_subscription:
    use_stripe()  # Great subscription support

# Need in-person payments? Square is best
if order.is_in_store:
    use_square()  # Best for point-of-sale

# Need international? PayPal is best
if customer.country not in ["USA", "UK", "CA"]:
    use_paypal()  # Supports 200+ countries
```

---

## 🎓 Real-World Scenario: Why You Need Adapters

### Scenario: Building a Video Streaming Platform

```python
# You need to store videos in the cloud
# But you want flexibility to use different providers

# Without Adapter Pattern:

def upload_video(video_file):
    if config.storage_provider == "aws":
        # AWS S3 SDK
        import boto3
        s3 = boto3.client('s3')
        s3.upload_fileobj(
            video_file,
            'my-bucket',
            'video.mp4',
            ExtraArgs={'ContentType': 'video/mp4'}
        )
    
    elif config.storage_provider == "google":
        # Google Cloud SDK
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket('my-bucket')
        blob = bucket.blob('video.mp4')
        blob.upload_from_file(video_file, content_type='video/mp4')
    
    elif config.storage_provider == "azure":
        # Azure SDK
        from azure.storage.blob import BlobServiceClient
        blob_service = BlobServiceClient.from_connection_string(conn_str)
        blob_client = blob_service.get_blob_client(
            container='my-bucket',
            blob='video.mp4'
        )
        blob_client.upload_blob(video_file, content_type='video/mp4')

# This is in EVERY function that touches cloud storage!
# upload_video(), download_video(), delete_video(), list_videos()
```

### With Adapter Pattern:

```python
# Define YOUR interface
class CloudStorage(ABC):
    @abstractmethod
    def upload(self, file, filename: str) -> str:
        """Upload file and return URL"""
        pass
    
    @abstractmethod
    def download(self, filename: str) -> bytes:
        """Download file"""
        pass
    
    @abstractmethod
    def delete(self, filename: str) -> bool:
        """Delete file"""
        pass

# Create adapters
class S3Adapter(CloudStorage):
    def __init__(self):
        self.s3 = boto3.client('s3')
    
    def upload(self, file, filename: str) -> str:
        self.s3.upload_fileobj(file, 'bucket', filename)
        return f"https://bucket.s3.amazonaws.com/{filename}"
    
    def download(self, filename: str) -> bytes:
        obj = self.s3.get_object(Bucket='bucket', Key=filename)
        return obj['Body'].read()
    
    def delete(self, filename: str) -> bool:
        self.s3.delete_object(Bucket='bucket', Key=filename)
        return True

class GoogleCloudAdapter(CloudStorage):
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket('bucket')
    
    def upload(self, file, filename: str) -> str:
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file)
        return blob.public_url
    
    def download(self, filename: str) -> bytes:
        blob = self.bucket.blob(filename)
        return blob.download_as_bytes()
    
    def delete(self, filename: str) -> bool:
        blob = self.bucket.blob(filename)
        blob.delete()
        return True

class AzureAdapter(CloudStorage):
    def __init__(self):
        self.blob_service = BlobServiceClient.from_connection_string(conn_str)
    
    def upload(self, file, filename: str) -> str:
        blob_client = self.blob_service.get_blob_client('container', filename)
        blob_client.upload_blob(file)
        return f"https://storage.blob.core.windows.net/container/{filename}"
    
    def download(self, filename: str) -> bytes:
        blob_client = self.blob_service.get_blob_client('container', filename)
        return blob_client.download_blob().readall()
    
    def delete(self, filename: str) -> bool:
        blob_client = self.blob_service.get_blob_client('container', filename)
        blob_client.delete_blob()
        return True

# Now your business logic is SIMPLE!
class VideoService:
    def __init__(self, storage: CloudStorage):
        self.storage = storage
    
    def upload_video(self, video_file, filename: str):
        url = self.storage.upload(video_file, filename)
        save_to_database(filename, url)
        return url
    
    def download_video(self, filename: str):
        return self.storage.download(filename)
    
    def delete_video(self, filename: str):
        self.storage.delete(filename)
        delete_from_database(filename)

# Easy to switch providers!
storage = get_storage_adapter(config.provider)
video_service = VideoService(storage)

# Or use different providers for different purposes
cdn_storage = S3Adapter()          # Fast for streaming
backup_storage = GoogleCloudAdapter()  # Cheap for backups
archive_storage = AzureAdapter()   # Long-term storage
```

---

## 🎯 Summary: Why Adapter Pattern Talks About SDKs

### The Core Problem

1. **Third-party SDKs are essential** - You can't build everything from scratch
2. **Every SDK is different** - Different companies, different designs
3. **You can't modify SDKs** - They're external libraries
4. **Your app needs consistency** - Can't have different code for each SDK

### The Solution

**Adapter Pattern lets you:**
- ✅ Use multiple third-party SDKs with a unified interface
- ✅ Switch providers without changing business logic
- ✅ Add new providers easily
- ✅ Keep your code clean and maintainable
- ✅ Isolate third-party dependencies

### Real-World Benefits

```python
# Without Adapters: Tightly coupled to SDKs
def process_payment(amount):
    if provider == "stripe":
        # 50 lines of Stripe-specific code
    elif provider == "paypal":
        # 50 lines of PayPal-specific code
    elif provider == "square":
        # 50 lines of Square-specific code
# Total: 150 lines per function!
# Multiply by 20 functions = 3,000 lines of messy code!

# With Adapters: Clean and simple
def process_payment(gateway: PaymentGateway, amount):
    return gateway.process_payment(amount)
# Total: 1 line!
# Adapters handle all the complexity separately
```

**Key Insight:** Modern applications rely on dozens of third-party services (payment, email, storage, SMS, analytics, etc.). Without the Adapter Pattern, your codebase would be an unmaintainable mess of SDK-specific code. Adapters give you **consistency** and **flexibility**! 🎯