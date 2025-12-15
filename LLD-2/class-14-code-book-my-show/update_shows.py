#!/usr/bin/env python
"""Update all shows to future times"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyshow.settings')
django.setup()

from bookmyshow.booking.models import Show
from django.utils import timezone
from datetime import timedelta

# Update all shows to future times
print("Updating shows to future times...")
for i, show in enumerate(Show.objects.all(), start=2):
    show.start_time = timezone.now() + timedelta(hours=i)
    show.save()
    print(f'{show.id}: starts at {show.start_time} (booking allowed: {show.is_booking_allowed()})')

print("\nDone! All shows updated.")
