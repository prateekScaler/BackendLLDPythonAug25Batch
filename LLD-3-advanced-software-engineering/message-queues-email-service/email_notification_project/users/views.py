"""
User API Views

This module contains API endpoints that trigger email notifications.
Each endpoint demonstrates how to use the Kafka producer to send
email requests asynchronously.

All endpoints:
1. Perform the main action (create user, place order, etc.)
2. Send email request to Kafka
3. Return immediately without waiting for email

The email is processed asynchronously by the email consumer service.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.kafka_producer import email_producer
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.

    POST /api/register/
    {
        "email": "user@example.com",
        "name": "John Doe",
        "password": "securepassword"
    }

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

        # In a real application:
        # 1. Validate email format
        # 2. Check if user already exists
        # 3. Hash password
        # 4. Create user in database
        user_id = str(uuid.uuid4())

        logger.info(f"Creating user: {email}")

        # Send welcome email request to Kafka (ASYNC!)
        email_data = {
            'type': 'welcome_email',
            'to': email,
            'data': {
                'user_id': user_id,
                'name': name,
                'email': email,
            }
        }

        success = email_producer.send_email_request(
            email_data,
            key=user_id  # Use user_id as partition key for ordering
        )

        if not success:
            logger.warning(f"Failed to queue welcome email for {email}")
            # Note: We still return success to the user
            # The email failure is logged and can be retried

        return Response({
            'status': 'success',
            'message': 'User registered successfully! Welcome email will be sent shortly.',
            'user_id': user_id
        }, status=status.HTTP_201_CREATED)


class PasswordResetView(APIView):
    """
    API endpoint for password reset requests.

    POST /api/password-reset/
    {
        "email": "user@example.com"
    }

    Sends a password reset email asynchronously via Kafka.
    Always returns success to prevent email enumeration attacks.
    """

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # In a real application:
        # 1. Check if user exists
        # 2. Generate secure reset token
        # 3. Store token with expiration
        # 4. Only send email if user exists
        reset_token = str(uuid.uuid4())

        logger.info(f"Password reset requested for: {email}")

        email_data = {
            'type': 'password_reset',
            'to': email,
            'data': {
                'reset_token': reset_token,
                'reset_link': f'https://yourapp.com/reset?token={reset_token}',
            }
        }

        email_producer.send_email_request(email_data)

        # Always return success to prevent email enumeration
        return Response({
            'status': 'success',
            'message': 'If the email exists, a reset link will be sent.'
        })


class OrderConfirmationView(APIView):
    """
    API endpoint for order confirmations.

    POST /api/order-confirm/
    {
        "email": "user@example.com",
        "order_id": "ORD-12345",
        "items": [
            {"name": "Widget A", "quantity": 2, "price": "$19.99"},
            {"name": "Gadget B", "quantity": 1, "price": "$49.99"}
        ],
        "total": "$89.97",
        "shipping_address": "123 Main St, City, State 12345"
    }

    Sends an order confirmation email asynchronously via Kafka.
    """

    def post(self, request):
        email = request.data.get('email')
        order_id = request.data.get('order_id', f'ORD-{uuid.uuid4().hex[:8].upper()}')
        items = request.data.get('items', [])
        total = request.data.get('total', '$0.00')
        shipping_address = request.data.get('shipping_address', 'Not provided')

        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Processing order {order_id} for {email}")

        # Format items for email
        items_list = '\n'.join([
            f"- {item.get('name', 'Item')} x{item.get('quantity', 1)} @ {item.get('price', 'N/A')}"
            for item in items
        ]) if items else 'No items'

        email_data = {
            'type': 'order_confirmation',
            'to': email,
            'data': {
                'order_id': order_id,
                'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'items': items,
                'items_list': items_list,
                'total': total,
                'shipping_address': shipping_address,
                'estimated_delivery': '3-5 business days',
            }
        }

        email_producer.send_email_request(email_data, key=order_id)

        return Response({
            'status': 'success',
            'message': 'Order placed! Confirmation email will be sent shortly.',
            'order_id': order_id
        })


class PaymentReceiptView(APIView):
    """
    API endpoint for payment receipts.

    POST /api/payment-receipt/
    {
        "email": "user@example.com",
        "amount": "$99.99",
        "transaction_id": "TXN-123456",
        "payment_method": "Credit Card ****1234"
    }

    Sends a payment receipt email asynchronously via Kafka.
    """

    def post(self, request):
        email = request.data.get('email')
        amount = request.data.get('amount', '$0.00')
        transaction_id = request.data.get('transaction_id', f'TXN-{uuid.uuid4().hex[:8].upper()}')
        payment_method = request.data.get('payment_method', 'Credit Card')
        description = request.data.get('description', 'Purchase')

        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Processing payment receipt {transaction_id} for {email}")

        email_data = {
            'type': 'payment_receipt',
            'to': email,
            'data': {
                'amount': amount,
                'transaction_id': transaction_id,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'payment_method': payment_method,
                'invoice_number': f'INV-{transaction_id}',
                'description': description,
            }
        }

        email_producer.send_email_request(email_data, key=transaction_id)

        return Response({
            'status': 'success',
            'message': 'Payment processed! Receipt will be sent shortly.',
            'transaction_id': transaction_id
        })


class ShippingUpdateView(APIView):
    """
    API endpoint for shipping updates.

    POST /api/shipping-update/
    {
        "email": "user@example.com",
        "order_id": "ORD-12345",
        "tracking_number": "1Z999AA10123456784",
        "carrier": "UPS"
    }

    Sends a shipping update email asynchronously via Kafka.
    """

    def post(self, request):
        email = request.data.get('email')
        order_id = request.data.get('order_id')
        tracking_number = request.data.get('tracking_number', 'N/A')
        carrier = request.data.get('carrier', 'Standard Shipping')
        shipping_address = request.data.get('shipping_address', 'On file')

        if not email or not order_id:
            return Response(
                {'error': 'Email and order_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Sending shipping update for order {order_id}")

        # Generate tracking link based on carrier
        tracking_links = {
            'UPS': f'https://www.ups.com/track?tracknum={tracking_number}',
            'FedEx': f'https://www.fedex.com/fedextrack/?trknbr={tracking_number}',
            'USPS': f'https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_number}',
        }
        tracking_link = tracking_links.get(carrier, f'https://track.example.com/{tracking_number}')

        email_data = {
            'type': 'order_shipped',
            'to': email,
            'data': {
                'order_id': order_id,
                'tracking_number': tracking_number,
                'carrier': carrier,
                'tracking_link': tracking_link,
                'shipping_address': shipping_address,
                'estimated_delivery': '2-3 business days',
            }
        }

        email_producer.send_email_request(email_data, key=order_id)

        return Response({
            'status': 'success',
            'message': 'Shipping update will be sent shortly.',
            'tracking_number': tracking_number
        })


class HealthCheckView(APIView):
    """
    Health check endpoint.

    GET /api/health/

    Returns the health status of the API and its dependencies.
    """

    def get(self, request):
        # Check Kafka connectivity
        kafka_healthy = False
        try:
            if email_producer._producer:
                # Try to get topic metadata as health check
                email_producer._producer.partitions_for('email-topic')
                kafka_healthy = True
        except Exception as e:
            logger.warning(f"Kafka health check failed: {e}")

        health_status = {
            'status': 'healthy' if kafka_healthy else 'degraded',
            'components': {
                'api': 'healthy',
                'kafka': 'healthy' if kafka_healthy else 'unhealthy'
            },
            'timestamp': datetime.now().isoformat()
        }

        status_code = status.HTTP_200_OK if kafka_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(health_status, status=status_code)
