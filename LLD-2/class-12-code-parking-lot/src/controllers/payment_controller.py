"""
Payment Controller - Handles HTTP requests for payment operations
"""

from typing import Dict, Any
from ..services import PaymentService
from ..enums import PaymentType
from ..exceptions import (
    TicketNotFoundException,
    PaymentAlreadyDoneException,
    PaymentNotFoundException
)


class PaymentController:
    """Controller for payment-related API endpoints"""

    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def process_payment(self, request_data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        """
        POST /payments
        Process payment for a ticket

        Request body:
        {
            "ticket_id": "TKT-12345",
            "payment_type": "UPI"
        }

        Returns: (response_dict, status_code)
        """
        try:
            # Validate request
            ticket_id = request_data.get('ticket_id')
            payment_type_str = request_data.get('payment_type')

            if not ticket_id:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'ticket_id is required'
                    }
                }, 400

            if not payment_type_str:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'payment_type is required'
                    }
                }, 400

            # Convert string to enum
            try:
                payment_type = PaymentType[payment_type_str.upper()]
            except KeyError:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'INVALID_PAYMENT_TYPE',
                        'message': f'Invalid payment type: {payment_type_str}. Valid: CASH, CREDIT_CARD, UPI'
                    }
                }, 400

            # Call service
            payment = self.payment_service.process_payment(
                ticket_id=ticket_id,
                payment_type=payment_type
            )

            # Format response
            return {
                'status': 'success',
                'data': {
                    'payment_id': payment.payment_id,
                    'ticket_id': payment.ticket_id,
                    'amount': payment.amount,
                    'payment_type': payment.payment_type.value,
                    'status': payment.status.value,
                    'payment_time': payment.payment_time.isoformat()
                }
            }, 200

        except TicketNotFoundException as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'TICKET_NOT_FOUND',
                    'message': str(e)
                }
            }, 404

        except PaymentAlreadyDoneException as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'PAYMENT_ALREADY_DONE',
                    'message': str(e)
                }
            }, 400

        except Exception as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'An unexpected error occurred'
                }
            }, 500

    def get_payment(self, ticket_id: str) -> tuple[Dict[str, Any], int]:
        """
        GET /payments/{ticket_id}
        Get payment details for a ticket

        Returns: (response_dict, status_code)
        """
        try:
            payment = self.payment_service.get_payment(ticket_id)

            return {
                'status': 'success',
                'data': {
                    'payment_id': payment.payment_id,
                    'ticket_id': payment.ticket_id,
                    'amount': payment.amount,
                    'payment_type': payment.payment_type.value,
                    'status': payment.status.value,
                    'payment_time': payment.payment_time.isoformat()
                }
            }, 200

        except PaymentNotFoundException as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'PAYMENT_NOT_FOUND',
                    'message': str(e)
                }
            }, 404

        except Exception as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'An unexpected error occurred'
                }
            }, 500

    def checkout(self, request_data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        """
        POST /checkout
        Generate invoice and complete checkout

        Request body:
        {
            "ticket_id": "TKT-12345",
            "exit_gate_id": "GATE-2"
        }

        Returns: (response_dict, status_code)
        """
        try:
            ticket_id = request_data.get('ticket_id')

            if not ticket_id:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'ticket_id is required'
                    }
                }, 400

            # Check if payment is done
            try:
                payment = self.payment_service.get_payment(ticket_id)
            except PaymentNotFoundException:
                return {
                    'status': 'error',
                    'error': {
                        'code': 'PAYMENT_NOT_DONE',
                        'message': 'Payment not completed for this ticket'
                    }
                }, 400

            # Generate invoice
            invoice = self.payment_service.generate_invoice(ticket_id)

            # Format response
            return {
                'status': 'success',
                'data': {
                    'invoice_id': invoice.invoice_id,
                    'ticket_id': invoice.ticket.ticket_id,
                    'entry_time': invoice.ticket.entry_time.isoformat(),
                    'exit_time': invoice.exit_time.isoformat(),
                    'duration_hours': round((invoice.exit_time - invoice.ticket.entry_time).total_seconds() / 3600, 2),
                    'amount': invoice.amount,
                    'payment_status': invoice.payment.status.value
                }
            }, 200

        except TicketNotFoundException as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'TICKET_NOT_FOUND',
                    'message': str(e)
                }
            }, 404

        except Exception as e:
            return {
                'status': 'error',
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'An unexpected error occurred'
                }
            }, 500
