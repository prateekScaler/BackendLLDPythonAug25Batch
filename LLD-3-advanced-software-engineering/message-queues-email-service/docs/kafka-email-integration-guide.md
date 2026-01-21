# Kafka + Django Email Service Integration Guide

A step-by-step guide to building an email notification service using Django, Apache Kafka, and SMTP.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Architecture](#project-architecture)
3. [Step 1: Install and Run Kafka](#step-1-install-and-run-kafka)
4. [Step 2: Setup Django Project](#step-2-setup-django-project)
5. [Step 3: Configure Kafka Producer](#step-3-configure-kafka-producer)
6. [Step 4: Create User Registration API](#step-4-create-user-registration-api)
7. [Step 5: Create Email Consumer](#step-5-create-email-consumer)
8. [Step 6: Setup SMTP Server](#step-6-setup-smtp-server)
9. [Step 7: Run and Test the System](#step-7-run-and-test-the-system)
10. [Step 8: Adding More Email Types](#step-8-adding-more-email-types)
11. [Production Considerations](#production-considerations)
12. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:
- Python 3.8+
- Docker and Docker Compose
- Basic understanding of Django
- A Gmail account (for SMTP testing)

---

## Project Architecture

```
┌──────────────┐      ┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Django     │      │   Kafka     │      │   Email      │      │   SMTP     │
│   API        │─────>│   Broker    │─────>│   Consumer   │─────>│   Server   │
│              │      │             │      │              │      │            │
│ POST /signup │      │ Topic:      │      │ Sends email  │      │ Gmail/     │
│ POST /order  │      │ email-topic │      │ via SMTP     │      │ SendGrid   │
└──────────────┘      └─────────────┘      └──────────────┘      └────────────┘
```

**Flow:**
1. User makes API request (signup, order, etc.)
2. Django API sends message to Kafka topic
3. API returns immediately to user
4. Email Consumer picks up message from Kafka
5. Consumer sends email via SMTP

---

## Step 1: Install and Run Kafka

### Option A: Using Docker (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

  # Optional: Kafka UI for visualization
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
```

Start Kafka:
```bash
docker-compose up -d
```

Verify Kafka is running:
```bash
docker-compose ps
# All services should show "Up"
```

### Option B: Manual Installation (macOS)

```bash
# Install with Homebrew
brew install kafka

# Start Zookeeper
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

# In another terminal, start Kafka
kafka-server-start /usr/local/etc/kafka/server.properties
```

### Option C: Manual Installation (Linux)

```bash
# Download Kafka
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xzf kafka_2.13-3.6.0.tgz
cd kafka_2.13-3.6.0

# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# In another terminal, start Kafka
bin/kafka-server-start.sh config/server.properties
```

### Create Kafka Topic (Optional - Auto-created by default)

```bash
# Using Docker
docker exec kafka kafka-topics --create --topic email-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

# Verify topic
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

---

## Step 2: Setup Django Project

### Create Virtual Environment

```bash
# Create project directory
mkdir email_notification_project
cd email_notification_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Install Dependencies

```bash
pip install django djangorestframework kafka-python python-dotenv
```

Create `requirements.txt`:
```
django>=4.2
djangorestframework>=3.14
kafka-python>=2.0.2
python-dotenv>=1.0.0
```

### Create Django Project

```bash
django-admin startproject config .
python manage.py startapp users
python manage.py startapp notifications
```

### Configure Settings

Edit `config/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'rest_framework',
    # Local apps
    'users',
    'notifications',
]

# Add at the bottom
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_EMAIL_TOPIC = 'email-topic'

# Email Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace
EMAIL_HOST_PASSWORD = 'your-app-password'  # Replace with App Password
DEFAULT_FROM_EMAIL = 'noreply@yourapp.com'
```

---

## Step 3: Configure Kafka Producer

Create `notifications/kafka_producer.py`:

```python
from kafka import KafkaProducer
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


class EmailProducer:
    """
    Kafka Producer for sending email requests to the email-topic.
    Uses singleton pattern to reuse the producer connection.
    """
    _instance = None
    _producer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._producer is None:
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8') if k else None,
                    acks='all',  # Wait for all replicas
                    retries=3,   # Retry on failure
                )
                logger.info("Kafka Producer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka Producer: {e}")
                raise

    def send_email_request(self, email_data: dict, key: str = None):
        """
        Send an email request to Kafka topic.

        Args:
            email_data: Dictionary containing email details
                - type: Email type (welcome, order_confirmation, etc.)
                - to: Recipient email address
                - subject: Email subject
                - data: Additional data for template
            key: Optional partition key (e.g., user_id for ordering)
        """
        try:
            future = self._producer.send(
                settings.KAFKA_EMAIL_TOPIC,
                value=email_data,
                key=key
            )
            # Block for 'synchronous' sends (optional)
            record_metadata = future.get(timeout=10)
            logger.info(
                f"Email request sent: topic={record_metadata.topic}, "
                f"partition={record_metadata.partition}, "
                f"offset={record_metadata.offset}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send email request: {e}")
            return False

    def close(self):
        """Close the producer connection."""
        if self._producer:
            self._producer.close()
            logger.info("Kafka Producer closed")


# Singleton instance
email_producer = EmailProducer()
```

---

## Step 4: Create User Registration API

### Create User Model (Optional - using Django's default)

Edit `users/views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.kafka_producer import email_producer
import uuid
import logging

logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    Sends a welcome email asynchronously via Kafka.
    """

    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')

        # Validation
        if not email or not name:
            return Response(
                {'error': 'Email and name are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # In real app: Create user in database
        user_id = str(uuid.uuid4())

        # Send welcome email request to Kafka (ASYNC!)
        email_data = {
            'type': 'welcome_email',
            'to': email,
            'subject': 'Welcome to Our Platform!',
            'data': {
                'user_id': user_id,
                'name': name,
            }
        }

        success = email_producer.send_email_request(
            email_data,
            key=user_id  # Use user_id as partition key
        )

        if not success:
            logger.warning(f"Failed to queue welcome email for {email}")
            # Note: We still return success - email will be retried or handled separately

        return Response({
            'status': 'success',
            'message': 'User registered successfully! Welcome email will be sent shortly.',
            'user_id': user_id
        }, status=status.HTTP_201_CREATED)


class PasswordResetView(APIView):
    """
    API endpoint for password reset.
    Sends a password reset email asynchronously via Kafka.
    """

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # In real app: Verify user exists, generate reset token
        reset_token = str(uuid.uuid4())

        email_data = {
            'type': 'password_reset',
            'to': email,
            'subject': 'Password Reset Request',
            'data': {
                'reset_token': reset_token,
                'reset_link': f'https://yourapp.com/reset?token={reset_token}',
            }
        }

        email_producer.send_email_request(email_data)

        return Response({
            'status': 'success',
            'message': 'If the email exists, a reset link will be sent.'
        })


class OrderConfirmationView(APIView):
    """
    API endpoint for order confirmation.
    Sends an order confirmation email asynchronously via Kafka.
    """

    def post(self, request):
        email = request.data.get('email')
        order_id = request.data.get('order_id')
        items = request.data.get('items', [])
        total = request.data.get('total')

        if not email or not order_id:
            return Response(
                {'error': 'Email and order_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        email_data = {
            'type': 'order_confirmation',
            'to': email,
            'subject': f'Order Confirmation - #{order_id}',
            'data': {
                'order_id': order_id,
                'items': items,
                'total': total,
            }
        }

        email_producer.send_email_request(email_data, key=order_id)

        return Response({
            'status': 'success',
            'message': 'Order placed! Confirmation email will be sent shortly.',
            'order_id': order_id
        })
```

### Configure URLs

Edit `users/urls.py`:

```python
from django.urls import path
from .views import UserRegistrationView, PasswordResetView, OrderConfirmationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('order-confirm/', OrderConfirmationView.as_view(), name='order-confirm'),
]
```

Edit `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]
```

---

## Step 5: Create Email Consumer

Create `email_consumer.py` in the project root:

```python
#!/usr/bin/env python
"""
Email Consumer Service

Consumes email requests from Kafka and sends emails via SMTP.
Run this as a separate process alongside your Django server.

Usage:
    python email_consumer.py
"""

import os
import sys
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kafka import KafkaConsumer
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('email_consumer')

# Configuration - In production, use environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'email-topic')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'email-consumer-group')

# SMTP Configuration
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', 'your-email@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your-app-password')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@yourapp.com')


# Email Templates
EMAIL_TEMPLATES = {
    'welcome_email': {
        'subject': 'Welcome to Our Platform!',
        'body': '''
Hello {name}!

Welcome to our platform! We're excited to have you on board.

Here are some things you can do:
- Complete your profile
- Explore our features
- Connect with other users

If you have any questions, feel free to reach out to our support team.

Best regards,
The Team
        '''
    },
    'password_reset': {
        'subject': 'Password Reset Request',
        'body': '''
Hello,

We received a request to reset your password.

Click the link below to reset your password:
{reset_link}

This link will expire in 24 hours.

If you didn't request this, please ignore this email.

Best regards,
The Team
        '''
    },
    'order_confirmation': {
        'subject': 'Order Confirmation - #{order_id}',
        'body': '''
Thank you for your order!

Order ID: {order_id}
Total: {total}

Items:
{items_list}

We'll send you another email when your order ships.

Best regards,
The Team
        '''
    }
}


def get_email_content(email_type: str, data: dict) -> tuple:
    """
    Get email subject and body from template.

    Args:
        email_type: Type of email (welcome_email, password_reset, etc.)
        data: Data to fill in the template

    Returns:
        Tuple of (subject, body)
    """
    template = EMAIL_TEMPLATES.get(email_type)

    if not template:
        logger.warning(f"Unknown email type: {email_type}")
        return (
            data.get('subject', 'Notification'),
            data.get('body', 'You have a new notification.')
        )

    subject = template['subject'].format(**data)
    body = template['body'].format(
        **data,
        items_list='\n'.join([f"- {item}" for item in data.get('items', [])])
    )

    return subject, body


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send email using SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (plain text)

    Returns:
        True if sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach body
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {e}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def process_message(message: dict) -> bool:
    """
    Process a single email message from Kafka.

    Args:
        message: Message containing email details

    Returns:
        True if processed successfully, False otherwise
    """
    email_type = message.get('type', 'generic')
    to_email = message.get('to')
    data = message.get('data', {})

    if not to_email:
        logger.error("No recipient email in message")
        return False

    # Add common data
    data['name'] = data.get('name', 'User')

    # Get email content from template
    subject, body = get_email_content(email_type, data)

    # Override subject if provided in message
    if message.get('subject'):
        subject = message['subject']

    return send_email(to_email, subject, body)


def run_consumer():
    """
    Main consumer loop. Consumes messages from Kafka and sends emails.
    """
    logger.info(f"Starting Email Consumer...")
    logger.info(f"Kafka: {KAFKA_BOOTSTRAP_SERVERS}, Topic: {KAFKA_TOPIC}")

    # Create consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',  # Start from earliest if no offset
        enable_auto_commit=True,
        auto_commit_interval_ms=1000,
    )

    logger.info("Email Consumer started. Waiting for messages...")
    logger.info("Press Ctrl+C to exit")

    try:
        for message in consumer:
            logger.info(f"Received message: partition={message.partition}, offset={message.offset}")
            logger.debug(f"Message value: {message.value}")

            start_time = datetime.now()
            success = process_message(message.value)
            duration = (datetime.now() - start_time).total_seconds()

            if success:
                logger.info(f"Message processed successfully in {duration:.2f}s")
            else:
                logger.error(f"Failed to process message after {duration:.2f}s")
                # In production: send to dead letter queue

    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    finally:
        consumer.close()
        logger.info("Consumer closed")


if __name__ == '__main__':
    run_consumer()
```

---

## Step 6: Setup SMTP Server

### Option A: Gmail SMTP (Recommended for Testing)

1. **Enable 2-Step Verification:**
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security > 2-Step Verification > Enable

2. **Generate App Password:**
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security > App passwords
   - Select app: "Mail"
   - Select device: "Other" (enter "Django App")
   - Click "Generate"
   - Copy the 16-character password

3. **Update Configuration:**
   ```python
   # In email_consumer.py or .env file
   SMTP_HOST = 'smtp.gmail.com'
   SMTP_PORT = 587
   SMTP_USER = 'your-email@gmail.com'
   SMTP_PASSWORD = 'your-16-char-app-password'
   ```

### Option B: MailHog (Local Testing - No Real Emails)

Add to `docker-compose.yml`:
```yaml
  mailhog:
    image: mailhog/mailhog
    container_name: mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI
```

Update configuration:
```python
SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SMTP_USER = ''  # No auth needed
SMTP_PASSWORD = ''
```

View emails at: http://localhost:8025

### Option C: SendGrid (Production)

1. Create account at [SendGrid](https://sendgrid.com/)
2. Create API Key
3. Update configuration:
   ```python
   SMTP_HOST = 'smtp.sendgrid.net'
   SMTP_PORT = 587
   SMTP_USER = 'apikey'
   SMTP_PASSWORD = 'your-sendgrid-api-key'
   ```

---

## Step 7: Run and Test the System

### Start All Services

```bash
# Terminal 1: Start Kafka
docker-compose up

# Terminal 2: Apply migrations and start Django
python manage.py migrate
python manage.py runserver

# Terminal 3: Start Email Consumer
python email_consumer.py
```

### Test the APIs

**User Registration:**
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "John Doe",
    "password": "securepassword123"
  }'
```

Expected Response:
```json
{
    "status": "success",
    "message": "User registered successfully! Welcome email will be sent shortly.",
    "user_id": "abc123-..."
}
```

**Password Reset:**
```bash
curl -X POST http://localhost:8000/api/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

**Order Confirmation:**
```bash
curl -X POST http://localhost:8000/api/order-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "order_id": "ORD-12345",
    "items": ["Widget A", "Gadget B"],
    "total": "$99.99"
  }'
```

### Monitor Kafka

Using Kafka UI (if added to docker-compose):
- Open http://localhost:8080
- View topics, messages, consumer groups

Using command line:
```bash
# List topics
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# View messages in topic
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic email-topic \
  --from-beginning
```

---

## Step 8: Adding More Email Types

### Add New Template

In `email_consumer.py`, add to `EMAIL_TEMPLATES`:

```python
EMAIL_TEMPLATES = {
    # ... existing templates ...

    'payment_receipt': {
        'subject': 'Payment Receipt - {amount}',
        'body': '''
Thank you for your payment!

Amount: {amount}
Transaction ID: {transaction_id}
Date: {date}

This receipt confirms your payment has been processed.

Best regards,
The Team
        '''
    },

    'shipping_update': {
        'subject': 'Your Order Has Shipped!',
        'body': '''
Great news! Your order is on its way!

Order ID: {order_id}
Tracking Number: {tracking_number}
Carrier: {carrier}

Track your package: {tracking_link}

Best regards,
The Team
        '''
    }
}
```

### Send New Email Type

```python
# In your Django view or service
email_data = {
    'type': 'payment_receipt',
    'to': user_email,
    'data': {
        'amount': '$49.99',
        'transaction_id': 'TXN-123456',
        'date': '2024-01-15'
    }
}
email_producer.send_email_request(email_data)
```

---

## Production Considerations

### 1. Environment Variables

Create `.env` file:
```env
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=email-topic
KAFKA_GROUP_ID=email-consumer-group

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourapp.com
```

### 2. Error Handling and Dead Letter Queue

```python
MAX_RETRIES = 3

def process_with_retry(message):
    retries = message.get('_retry_count', 0)

    try:
        process_message(message)
    except Exception as e:
        if retries < MAX_RETRIES:
            message['_retry_count'] = retries + 1
            # Send back to main topic or retry topic
            producer.send('email-topic-retry', message)
        else:
            # Send to dead letter queue
            producer.send('email-topic-dlq', message)
            logger.error(f"Message sent to DLQ after {MAX_RETRIES} retries")
```

### 3. Monitoring

Add metrics tracking:
```python
from prometheus_client import Counter, Histogram

emails_sent = Counter('emails_sent_total', 'Total emails sent', ['type', 'status'])
email_duration = Histogram('email_send_duration_seconds', 'Time to send email')

@email_duration.time()
def send_email(to_email, subject, body):
    # ... send logic ...
    emails_sent.labels(type='welcome', status='success').inc()
```

### 4. Health Check Endpoint

```python
# In Django views
class HealthCheckView(APIView):
    def get(self, request):
        # Check Kafka connectivity
        try:
            email_producer._producer.partitions_for('email-topic')
            kafka_healthy = True
        except:
            kafka_healthy = False

        return Response({
            'status': 'healthy' if kafka_healthy else 'unhealthy',
            'kafka': kafka_healthy
        })
```

### 5. Scaling Consumers

Run multiple consumer instances:
```bash
# Terminal 1
python email_consumer.py

# Terminal 2
python email_consumer.py

# Terminal 3
python email_consumer.py
```

All consumers with the same `group_id` will share the load!

---

## Troubleshooting

### Kafka Connection Issues

```bash
# Check if Kafka is running
docker-compose ps

# Check Kafka logs
docker-compose logs kafka

# Test connectivity
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Consumer Not Receiving Messages

1. Check topic exists:
   ```bash
   docker exec kafka kafka-topics --describe --topic email-topic --bootstrap-server localhost:9092
   ```

2. Check consumer group:
   ```bash
   docker exec kafka kafka-consumer-groups --describe --group email-consumer-group --bootstrap-server localhost:9092
   ```

3. Reset consumer offset:
   ```bash
   docker exec kafka kafka-consumer-groups --reset-offsets --group email-consumer-group --topic email-topic --to-earliest --execute --bootstrap-server localhost:9092
   ```

### SMTP Authentication Failed

1. Verify Gmail App Password is correct
2. Check if 2-Step Verification is enabled
3. Try generating a new App Password
4. Check if "Less secure app access" needs to be enabled (not recommended)

### Messages Stuck in Queue

1. Check consumer logs for errors
2. Verify consumer is running
3. Check consumer group lag:
   ```bash
   docker exec kafka kafka-consumer-groups --describe --group email-consumer-group --bootstrap-server localhost:9092
   ```

---

## Summary

You now have a working email notification system with:
- Django REST API for triggering emails
- Kafka for reliable message queuing
- Separate consumer service for sending emails
- SMTP integration for actual email delivery

**Next Steps:**
- Add more email types and templates
- Implement HTML email templates
- Add rate limiting
- Set up monitoring and alerting
- Deploy to production with managed Kafka (Confluent Cloud, AWS MSK)
