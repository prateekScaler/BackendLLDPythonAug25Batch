"""
Email Templates

This module contains all email templates used by the email consumer service.
Templates use Python string formatting with placeholders like {name}, {order_id}, etc.

To add a new email type:
1. Add a new entry to EMAIL_TEMPLATES dictionary
2. Define 'subject' and 'body' with appropriate placeholders
3. Use the new type in your API: {'type': 'your_new_type', ...}
"""

EMAIL_TEMPLATES = {
    # ==========================================================================
    # USER ACCOUNT EMAILS
    # ==========================================================================

    'welcome_email': {
        'subject': 'Welcome to Our Platform, {name}!',
        'body': '''
Hello {name}!

Welcome to our platform! We're thrilled to have you join our community.

Here are some things you can do to get started:

1. Complete Your Profile
   Add a profile picture and tell us about yourself.

2. Explore Our Features
   Check out our dashboard to see what's available.

3. Connect With Others
   Find and follow other users with similar interests.

4. Get Help
   Visit our help center or contact support anytime.

Your account details:
- User ID: {user_id}
- Email: {email}

If you have any questions, don't hesitate to reach out!

Best regards,
The Team

---
You received this email because you signed up for an account.
        '''.strip()
    },

    'password_reset': {
        'subject': 'Password Reset Request',
        'body': '''
Hello,

We received a request to reset your password for your account.

Click the link below to reset your password:
{reset_link}

This link will expire in 24 hours for security reasons.

If you didn't request a password reset, you can safely ignore this email.
Your password will remain unchanged.

For security tips:
- Never share your password with anyone
- Use a unique password for each account
- Enable two-factor authentication if available

Best regards,
The Security Team

---
This is an automated message. Please do not reply directly to this email.
        '''.strip()
    },

    'email_verification': {
        'subject': 'Please Verify Your Email Address',
        'body': '''
Hello {name},

Thank you for registering! Please verify your email address to complete
your account setup.

Click the link below to verify your email:
{verification_link}

This link will expire in 48 hours.

If you didn't create an account, please ignore this email.

Best regards,
The Team
        '''.strip()
    },

    'account_deactivated': {
        'subject': 'Your Account Has Been Deactivated',
        'body': '''
Hello {name},

Your account has been deactivated as requested.

If you change your mind, you can reactivate your account within 30 days
by logging in with your credentials.

After 30 days, your account and all associated data will be permanently
deleted.

If you didn't request this deactivation, please contact support immediately.

Best regards,
The Team
        '''.strip()
    },

    # ==========================================================================
    # ORDER & COMMERCE EMAILS
    # ==========================================================================

    'order_confirmation': {
        'subject': 'Order Confirmation - #{order_id}',
        'body': '''
Thank you for your order!

We've received your order and it's being processed.

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

WHAT'S NEXT?
------------
1. We'll send you an email when your order ships
2. You can track your order status in your account
3. Estimated delivery: {estimated_delivery}

Questions about your order? Contact our support team.

Thank you for shopping with us!

Best regards,
The Team

---
Order #{order_id} | Placed on {order_date}
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

ESTIMATED DELIVERY
------------------
{estimated_delivery}

SHIPPING ADDRESS
----------------
{shipping_address}

If you have any questions about your delivery, please contact the carrier
directly or reach out to our support team.

Thank you for your order!

Best regards,
The Team
        '''.strip()
    },

    'order_delivered': {
        'subject': 'Your Order Has Been Delivered - #{order_id}',
        'body': '''
Hello {name},

Your order has been delivered!

ORDER DETAILS
-------------
Order ID: #{order_id}
Delivered: {delivery_date}

We hope you love your purchase! If you have a moment, we'd appreciate
if you could leave a review.

Need to return something?
You have 30 days from delivery to initiate a return.

Thank you for shopping with us!

Best regards,
The Team
        '''.strip()
    },

    # ==========================================================================
    # PAYMENT EMAILS
    # ==========================================================================

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

This receipt confirms your payment has been processed successfully.

For your records:
- Invoice Number: {invoice_number}
- Description: {description}

If you have any questions about this payment, please contact our
billing team with your transaction ID.

Best regards,
The Billing Team

---
Transaction ID: {transaction_id}
        '''.strip()
    },

    'payment_failed': {
        'subject': 'Payment Failed - Action Required',
        'body': '''
Hello {name},

We were unable to process your payment.

FAILED PAYMENT DETAILS
----------------------
Amount: {amount}
Date: {date}
Reason: {failure_reason}

WHAT TO DO NEXT
---------------
1. Check that your payment information is correct
2. Ensure sufficient funds are available
3. Try again or use a different payment method

Update your payment method:
{update_payment_link}

If you continue to experience issues, please contact our support team.

Best regards,
The Billing Team
        '''.strip()
    },

    'refund_processed': {
        'subject': 'Refund Processed - {amount}',
        'body': '''
Hello {name},

Your refund has been processed.

REFUND DETAILS
--------------
Amount: {amount}
Transaction ID: {transaction_id}
Original Order: #{order_id}
Refund Date: {date}

The refund will appear on your original payment method within 5-10
business days, depending on your bank.

If you don't see the refund after 10 business days, please contact
your bank first, then reach out to us if needed.

Best regards,
The Billing Team
        '''.strip()
    },

    # ==========================================================================
    # NOTIFICATION EMAILS
    # ==========================================================================

    'new_login_alert': {
        'subject': 'New Login Detected on Your Account',
        'body': '''
Hello {name},

We detected a new login to your account.

LOGIN DETAILS
-------------
Date: {login_date}
Location: {location}
Device: {device}
IP Address: {ip_address}

If this was you, you can ignore this email.

If you don't recognize this activity:
1. Change your password immediately
2. Enable two-factor authentication
3. Review your recent account activity
4. Contact support if you need help

Secure your account:
{security_link}

Best regards,
The Security Team
        '''.strip()
    },

    'subscription_renewal': {
        'subject': 'Your Subscription Will Renew Soon',
        'body': '''
Hello {name},

This is a reminder that your subscription will automatically renew.

SUBSCRIPTION DETAILS
--------------------
Plan: {plan_name}
Renewal Date: {renewal_date}
Amount: {amount}

Your subscription will automatically renew unless you cancel before
the renewal date.

Manage your subscription:
{manage_subscription_link}

Thank you for being a subscriber!

Best regards,
The Team
        '''.strip()
    },

    # ==========================================================================
    # GENERIC / CUSTOM
    # ==========================================================================

    'generic_notification': {
        'subject': '{subject}',
        'body': '''
Hello {name},

{message}

Best regards,
The Team
        '''.strip()
    },
}


def get_template(email_type: str) -> dict:
    """
    Get email template by type.

    Args:
        email_type: The type of email template to retrieve

    Returns:
        Dictionary with 'subject' and 'body' keys, or None if not found
    """
    return EMAIL_TEMPLATES.get(email_type)


def render_template(email_type: str, data: dict) -> tuple:
    """
    Render email template with provided data.

    Args:
        email_type: The type of email template
        data: Dictionary of values to fill in the template

    Returns:
        Tuple of (subject, body) with placeholders filled in

    Raises:
        KeyError: If required placeholder is missing from data
    """
    template = get_template(email_type)

    if not template:
        # Return generic template for unknown types
        return (
            data.get('subject', 'Notification'),
            data.get('body', data.get('message', 'You have a new notification.'))
        )

    # Fill in placeholders
    subject = template['subject'].format(**data)
    body = template['body'].format(**data)

    return subject, body


def list_available_templates() -> list:
    """
    Get list of available email template types.

    Returns:
        List of template type names
    """
    return list(EMAIL_TEMPLATES.keys())
