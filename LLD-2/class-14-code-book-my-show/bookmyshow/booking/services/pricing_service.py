"""
Pricing Service
Dynamic pricing logic for seat prices

Interview Points:
- Business logic separation
- Dynamic pricing strategies
- Rule-based systems
"""
from decimal import Decimal
from ..models import PricingRule, SeatType
from .base_service import BaseService


class PricingService(BaseService):
    """
    Service for calculating seat prices dynamically

    Interview Note: Pricing can be complex based on multiple factors
    - Seat type (Gold/Diamond/Platinum)
    - Day of week (Weekend surge pricing)
    - Time of day (Prime time pricing)
    - Movie popularity (Blockbuster pricing)
    - Theater location (Premium locations)
    """

    @staticmethod
    def calculate_seat_price(show, seat):
        """
        Calculate price for a seat in a show

        Interview Question: How do you design flexible pricing?
        Answer: Rule-based system with multipliers

        Flow:
        1. Start with base price
        2. Apply seat type multiplier
        3. Apply day of week multiplier
        4. Apply time of day multiplier
        5. Apply movie/theater specific rules

        Example:
        Base: $100
        Seat (Platinum): 1.5x = $150
        Weekend: 1.2x = $180
        Prime time: 1.3x = $234
        """
        base_price = Decimal('100.00')  # Default base price

        # Get applicable pricing rules
        rules = PricingRule.objects.filter(
            is_active=True
        ).filter(
            # Match specific criteria or NULL (applies to all)
            Q(theater=show.theater) | Q(theater__isnull=True),
            Q(movie=show.movie) | Q(movie__isnull=True),
            Q(seat_type=seat.seat_type) | Q(seat_type__isnull=True),
        )

        # Apply most specific rule first
        total_multiplier = Decimal('1.0')

        # Seat type multiplier
        seat_rule = rules.filter(seat_type=seat.seat_type).first()
        if seat_rule:
            base_price = seat_rule.base_price
            total_multiplier *= seat_rule.seat_multiplier

        # Day of week multiplier
        day_of_week = show.start_time.weekday()  # 0=Monday, 6=Sunday
        day_rule = rules.filter(day_of_week=day_of_week).first()
        if day_rule:
            total_multiplier *= day_rule.day_multiplier

        # Time of day multiplier
        hour = show.start_time.hour
        time_rule = rules.filter(
            start_hour__lte=hour,
            end_hour__gt=hour
        ).first()
        if time_rule:
            total_multiplier *= time_rule.time_multiplier

        # Theater/Movie specific rules
        specific_rule = rules.filter(
            theater=show.theater,
            movie=show.movie
        ).first()
        if specific_rule:
            base_price = specific_rule.base_price

        final_price = base_price * total_multiplier

        return final_price.quantize(Decimal('0.01'))  # Round to 2 decimal places

    @staticmethod
    def create_default_pricing_rules():
        """
        Create default pricing rules

        Interview Note: Initialize system with sensible defaults
        """
        from django.db.models import Q

        rules = [
            # Seat type based pricing
            PricingRule(
                id='RULE-GOLD',
                name='Gold Seat Base Price',
                base_price=Decimal('100.00'),
                seat_type=SeatType.GOLD,
                seat_multiplier=Decimal('1.0')
            ),
            PricingRule(
                id='RULE-DIAMOND',
                name='Diamond Seat Base Price',
                base_price=Decimal('100.00'),
                seat_type=SeatType.DIAMOND,
                seat_multiplier=Decimal('1.3')
            ),
            PricingRule(
                id='RULE-PLATINUM',
                name='Platinum Seat Base Price',
                base_price=Decimal('100.00'),
                seat_type=SeatType.PLATINUM,
                seat_multiplier=Decimal('1.5')
            ),

            # Weekend surge pricing
            PricingRule(
                id='RULE-SATURDAY',
                name='Saturday Surge',
                base_price=Decimal('100.00'),
                day_of_week=5,  # Saturday
                day_multiplier=Decimal('1.2')
            ),
            PricingRule(
                id='RULE-SUNDAY',
                name='Sunday Surge',
                base_price=Decimal('100.00'),
                day_of_week=6,  # Sunday
                day_multiplier=Decimal('1.2')
            ),

            # Prime time pricing (6 PM - 10 PM)
            PricingRule(
                id='RULE-PRIMETIME',
                name='Prime Time Pricing',
                base_price=Decimal('100.00'),
                start_hour=18,
                end_hour=22,
                time_multiplier=Decimal('1.3')
            ),
        ]

        PricingRule.objects.bulk_create(rules, ignore_conflicts=True)

        return len(rules)


# Import Q for pricing_service
from django.db.models import Q
