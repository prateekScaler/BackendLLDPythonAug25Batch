"""
App configuration for booking app
"""
from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookmyshow.booking'
    verbose_name = 'BookMyShow Booking'
