#!/usr/bin/env python
"""
Email Consumer Service

This is a standalone consumer that:
1. Connects to Kafka
2. Consumes messages from the email-topic
3. Sends emails via SMTP

Run this as a separate process alongside your Django server:
    python email_consumer.py

For production, run multiple instances for scalability:
    python email_consumer.py &
    python email_consumer.py &
    python email_consumer.py &

All instances with the same group_id will share the load automatically.

Configuration via environment variables:
    KAFKA_BOOTSTRAP_SERVERS - Kafka broker addresses (default: localhost:9092)
    KAFKA_TOPIC - Topic to consume from (default: email-topic)
    KAFKA_GROUP_ID - Consumer group ID (default: email-consumer-group)
    SMTP_HOST - SMTP server host (default: smtp.gmail.com)
    SMTP_PORT - SMTP server port (default: 587)
    SMTP_USER - SMTP username
    SMTP_PASSWORD - SMTP password
    FROM_EMAIL - From email address
"""

import os
import sys
import json
import logging
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('email_consumer')

# Try to import kafka-python
try:
    from kafka import KafkaConsumer
    from kafka.errors import KafkaError
except ImportError:
    logger.error("kafka-python not installed. Run: pip install kafka-python")
    sys.exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'email-topic')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'email-consumer-group')

# SMTP Configuration
SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')  # Use 'localhost' for MailHog, 'smtp.gmail.com' for Gmail
SMTP_PORT = int(os.getenv('SMTP_PORT', 1025))    # Use 1025 for MailHog, 587 for Gmail
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@yourapp.com')

# Use TLS for production SMTP servers
USE_TLS = SMTP_PORT == 587


# =============================================================================
# EMAIL TEMPLATES
# =============================================================================

EMAIL_TEMPLATES = {
    'welcome_email': {
        'subject': 'Welcome to Our Platform, {name}!',
        'body': '''
Hello {name}!

Welcome to our platform! We're thrilled to have you join our community.

Here are some things you can do to get started:
1. Complete Your Profile
2. Explore Our Features
3. Connect With Others

Your account details:
- User ID: {user_id}
- Email: {email}

If you have any questions, don't hesitate to reach out!

Best regards,
The Team
        '''.strip()
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
The Security Team
        '''.strip()
    },

    'order_confirmation': {
        'subject': 'Order Confirmation - #{order_id}',
        'body': '''
Thank you for your order!

ORDER DETAILS
-------------
Order ID: #{order_id}
Order Date: {order_date}
Total: {total}

ITEMS ORDERED
-------------
{items_list}

SHIPPING ADDRESS
----------------
{shipping_address}

Estimated delivery: {estimated_delivery}

Thank you for shopping with us!

Best regards,
The Team
        '''.strip()
    },

    'order_shipped': {
        'subject': 'Your Order Has Shipped! - #{order_id}',
        'body': '''
Great news! Your order is on its way!

SHIPPING DETAILS
----------------
Order ID: #{order_id}
Carrier: {carrier}
Tracking Number: {tracking_number}

Track your package:
{tracking_link}

Estimated delivery: {estimated_delivery}

Thank you for your order!

Best regards,
The Team
        '''.strip()
    },

    'payment_receipt': {
        'subject': 'Payment Receipt - {amount}',
        'body': '''
Thank you for your payment!

PAYMENT DETAILS
---------------
Amount: {amount}
Transaction ID: {transaction_id}
Date: {date}
Payment Method: {payment_method}
Invoice: {invoice_number}
Description: {description}

This receipt confirms your payment has been processed.

Best regards,
The Billing Team
        '''.strip()
    },
}


# =============================================================================
# EMAIL FUNCTIONS
# =============================================================================

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
        logger.warning(f"Unknown email type: {email_type}, using generic template")
        return (
            data.get('subject', 'Notification'),
            data.get('body', data.get('message', 'You have a new notification.'))
        )

    # Add default values for missing fields
    defaults = {
        'name': 'User',
        'user_id': 'N/A',
        'email': 'N/A',
        'reset_link': 'N/A',
        'order_id': 'N/A',
        'order_date': datetime.now().strftime('%Y-%m-%d'),
        'total': 'N/A',
        'items_list': 'No items',
        'shipping_address': 'N/A',
        'estimated_delivery': '3-5 business days',
        'carrier': 'N/A',
        'tracking_number': 'N/A',
        'tracking_link': 'N/A',
        'amount': 'N/A',
        'transaction_id': 'N/A',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'payment_method': 'N/A',
        'invoice_number': 'N/A',
        'description': 'N/A',
    }

    # Merge defaults with provided data
    merged_data = {**defaults, **data}

    try:
        subject = template['subject'].format(**merged_data)
        body = template['body'].format(**merged_data)
        return subject, body
    except KeyError as e:
        logger.error(f"Missing template variable: {e}")
        return (data.get('subject', 'Notification'), str(merged_data))


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
            if USE_TLS:
                server.starttls()
            if SMTP_USER and SMTP_PASSWORD:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {e}")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        logger.error(f"Recipient refused: {e}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        return False
    except ConnectionRefusedError:
        logger.error(f"Connection refused to {SMTP_HOST}:{SMTP_PORT}. Is the SMTP server running?")
        return False
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def process_message(message: dict) -> bool:
    """
    Process a single email message from Kafka.

    Args:
        message: Message containing email details
            - type: Email type (welcome_email, etc.)
            - to: Recipient email
            - data: Template data

    Returns:
        True if processed successfully, False otherwise
    """
    email_type = message.get('type', 'generic')
    to_email = message.get('to')
    data = message.get('data', {})

    if not to_email:
        logger.error("No recipient email in message")
        return False

    logger.info(f"Processing {email_type} email for {to_email}")

    # Get email content from template
    subject, body = get_email_content(email_type, data)

    # Override subject if explicitly provided
    if message.get('subject'):
        subject = message['subject']

    return send_email(to_email, subject, body)


# =============================================================================
# CONSUMER
# =============================================================================

def create_consumer():
    """
    Create and configure Kafka consumer.

    Returns:
        KafkaConsumer instance
    """
    logger.info(f"Creating consumer for topic '{KAFKA_TOPIC}'")
    logger.info(f"Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
    logger.info(f"Consumer group: {KAFKA_GROUP_ID}")

    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',      # Start from earliest if no offset
        enable_auto_commit=True,           # Auto-commit offsets
        auto_commit_interval_ms=1000,      # Commit every second
        max_poll_interval_ms=300000,       # 5 minutes max processing time
        session_timeout_ms=10000,          # 10 seconds session timeout
        heartbeat_interval_ms=3000,        # 3 seconds heartbeat
    )


def run_consumer():
    """
    Main consumer loop.

    Consumes messages from Kafka and sends emails.
    Runs indefinitely until interrupted.
    """
    logger.info("=" * 60)
    logger.info("EMAIL CONSUMER SERVICE")
    logger.info("=" * 60)
    logger.info(f"Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
    logger.info(f"Topic: {KAFKA_TOPIC}")
    logger.info(f"Group: {KAFKA_GROUP_ID}")
    logger.info(f"SMTP: {SMTP_HOST}:{SMTP_PORT}")
    logger.info("=" * 60)

    consumer = None
    retry_count = 0
    max_retries = 5

    while retry_count < max_retries:
        try:
            consumer = create_consumer()
            logger.info("Consumer connected successfully!")
            logger.info("Waiting for messages... (Press Ctrl+C to exit)")
            logger.info("-" * 60)

            retry_count = 0  # Reset retry count on successful connection

            for message in consumer:
                logger.info(
                    f"Received message: "
                    f"partition={message.partition}, "
                    f"offset={message.offset}"
                )

                start_time = datetime.now()

                try:
                    success = process_message(message.value)
                    duration = (datetime.now() - start_time).total_seconds()

                    if success:
                        logger.info(f"Message processed successfully in {duration:.2f}s")
                    else:
                        logger.error(f"Failed to process message after {duration:.2f}s")
                        # In production: send to dead letter queue

                except Exception as e:
                    logger.error(f"Error processing message: {e}")

                logger.info("-" * 60)

        except KafkaError as e:
            retry_count += 1
            logger.error(f"Kafka error: {e}")
            logger.info(f"Retrying in 5 seconds... ({retry_count}/{max_retries})")
            time.sleep(5)

        except KeyboardInterrupt:
            logger.info("\nShutdown requested...")
            break

        except Exception as e:
            retry_count += 1
            logger.error(f"Unexpected error: {e}")
            logger.info(f"Retrying in 5 seconds... ({retry_count}/{max_retries})")
            time.sleep(5)

        finally:
            if consumer:
                consumer.close()
                logger.info("Consumer closed")

    if retry_count >= max_retries:
        logger.error(f"Max retries ({max_retries}) exceeded. Exiting.")
        sys.exit(1)

    logger.info("Email Consumer Service stopped")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                  EMAIL CONSUMER SERVICE                       ║
    ║                                                               ║
    ║  This service consumes email requests from Kafka and sends    ║
    ║  emails via SMTP.                                             ║
    ║                                                               ║
    ║  Make sure Kafka is running before starting this service.     ║
    ║  Use docker-compose up to start Kafka and MailHog.            ║
    ║                                                               ║
    ║  View emails at: http://localhost:8025 (MailHog)              ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    run_consumer()
