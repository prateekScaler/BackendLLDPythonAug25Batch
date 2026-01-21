"""
Kafka Producer for Email Notifications

This module provides a singleton Kafka producer for sending email requests
to the email-topic. Messages are serialized as JSON and sent asynchronously.

Usage:
    from notifications.kafka_producer import email_producer

    email_producer.send_email_request({
        'type': 'welcome_email',
        'to': 'user@example.com',
        'subject': 'Welcome!',
        'data': {'name': 'John'}
    })
"""

from kafka import KafkaProducer
from kafka.errors import KafkaError
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


class EmailProducer:
    """
    Kafka Producer for sending email requests to the email-topic.

    Uses singleton pattern to reuse the producer connection across requests.
    Messages are automatically serialized to JSON.

    Attributes:
        _instance: Singleton instance
        _producer: Kafka producer instance
    """
    _instance = None
    _producer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._producer is None:
            self._initialize_producer()

    def _initialize_producer(self):
        """Initialize the Kafka producer with configuration."""
        try:
            self._producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',           # Wait for all replicas to acknowledge
                retries=3,            # Retry on transient failures
                retry_backoff_ms=100, # Wait between retries
                max_block_ms=5000,    # Max time to block on send
            )
            logger.info(
                f"Kafka Producer initialized successfully. "
                f"Servers: {settings.KAFKA_BOOTSTRAP_SERVERS}"
            )
        except KafkaError as e:
            logger.error(f"Failed to initialize Kafka Producer: {e}")
            # Don't raise - allow the app to run even if Kafka is down
            # Messages will be logged as failed
            self._producer = None

    def send_email_request(self, email_data: dict, key: str = None) -> bool:
        """
        Send an email request to Kafka topic.

        The message will be picked up by the email consumer service and
        processed asynchronously.

        Args:
            email_data: Dictionary containing email details
                - type: Email type (welcome_email, order_confirmation, etc.)
                - to: Recipient email address
                - subject: Email subject (optional, can use template default)
                - data: Additional data for template rendering
            key: Optional partition key (e.g., user_id for ordering)
                 Messages with the same key go to the same partition

        Returns:
            True if message was sent successfully, False otherwise

        Example:
            email_producer.send_email_request({
                'type': 'welcome_email',
                'to': 'user@example.com',
                'data': {
                    'user_id': '123',
                    'name': 'John Doe'
                }
            }, key='user-123')
        """
        if self._producer is None:
            logger.error("Kafka Producer not initialized. Message not sent.")
            self._log_failed_message(email_data)
            return False

        try:
            # Send message to Kafka
            future = self._producer.send(
                settings.KAFKA_EMAIL_TOPIC,
                value=email_data,
                key=key
            )

            # Wait for acknowledgment (with timeout)
            record_metadata = future.get(timeout=10)

            logger.info(
                f"Email request sent successfully: "
                f"topic={record_metadata.topic}, "
                f"partition={record_metadata.partition}, "
                f"offset={record_metadata.offset}, "
                f"type={email_data.get('type')}, "
                f"to={email_data.get('to')}"
            )
            return True

        except KafkaError as e:
            logger.error(f"Kafka error sending email request: {e}")
            self._log_failed_message(email_data)
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email request: {e}")
            self._log_failed_message(email_data)
            return False

    def send_email_request_async(self, email_data: dict, key: str = None):
        """
        Send an email request asynchronously (fire-and-forget).

        Use this when you don't need to wait for confirmation.
        Faster but less reliable than send_email_request().

        Args:
            email_data: Dictionary containing email details
            key: Optional partition key
        """
        if self._producer is None:
            logger.error("Kafka Producer not initialized. Message not sent.")
            return

        def on_success(record_metadata):
            logger.debug(
                f"Email request sent: partition={record_metadata.partition}, "
                f"offset={record_metadata.offset}"
            )

        def on_error(exception):
            logger.error(f"Failed to send email request: {exception}")
            self._log_failed_message(email_data)

        try:
            future = self._producer.send(
                settings.KAFKA_EMAIL_TOPIC,
                value=email_data,
                key=key
            )
            future.add_callback(on_success)
            future.add_errback(on_error)
        except Exception as e:
            logger.error(f"Error queuing email request: {e}")

    def _log_failed_message(self, email_data: dict):
        """
        Log failed messages for manual processing or retry.

        In production, you might want to:
        - Save to database for retry
        - Send to a dead letter queue
        - Alert operations team
        """
        logger.warning(
            f"FAILED_EMAIL_REQUEST: type={email_data.get('type')}, "
            f"to={email_data.get('to')}, "
            f"data={email_data}"
        )

    def flush(self):
        """Flush all pending messages. Call before shutdown."""
        if self._producer:
            self._producer.flush()
            logger.info("Kafka Producer flushed")

    def close(self):
        """Close the producer connection."""
        if self._producer:
            self._producer.close()
            self._producer = None
            logger.info("Kafka Producer closed")


# Singleton instance - import this in your views
email_producer = EmailProducer()
