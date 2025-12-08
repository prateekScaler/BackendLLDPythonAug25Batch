from abc import ABC, abstractmethod
from datetime import datetime
from ..enums import SpotType
import math


class PricingStrategy(ABC):
    """Abstract base class for pricing strategies"""

    @abstractmethod
    def calculate_fee(self, entry_time: datetime, exit_time: datetime, spot_type: SpotType) -> float:
        """Calculate parking fee based on duration and spot type"""
        pass


class HourlyPricingStrategy(PricingStrategy):
    """Hourly pricing strategy with different rates for different spot types"""

    # Pricing: {spot_type: (first_hour_rate, additional_hour_rate)}
    PRICING_TABLE = {
        SpotType.SMALL: (50, 80),
        SpotType.MEDIUM: (80, 100),
        SpotType.LARGE: (100, 120),
    }

    def calculate_fee(self, entry_time: datetime, exit_time: datetime, spot_type: SpotType) -> float:
        """Calculate fee based on hourly rates"""
        duration = exit_time - entry_time
        hours = math.ceil(duration.total_seconds() / 3600)  # Round up to nearest hour

        if hours <= 0:
            hours = 1  # Minimum 1 hour charge

        first_hour_rate, additional_hour_rate = self.PRICING_TABLE.get(spot_type, (50, 80))

        if hours == 1:
            return first_hour_rate
        else:
            return first_hour_rate + (hours - 1) * additional_hour_rate
