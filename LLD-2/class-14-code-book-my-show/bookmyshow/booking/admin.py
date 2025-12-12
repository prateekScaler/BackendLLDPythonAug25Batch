"""
Django Admin Configuration for BookMyShow
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    City, Theater, Screen, Seat, Movie, Show, ShowSeat,
    User, Ticket, TicketSeat, Payment, PricingRule, Coupon
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'created_at']
    list_filter = ['city']
    search_fields = ['name', 'city__name']


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'theater', 'created_at']
    list_filter = ['theater__city', 'theater']
    search_fields = ['name', 'theater__name']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'seat_type', 'screen', 'created_at']
    list_filter = ['seat_type', 'screen__theater']
    search_fields = ['number', 'screen__name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rating', 'category', 'duration', 'created_at']
    list_filter = ['category', 'rating']
    search_fields = ['name', 'category']


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'theater', 'screen', 'start_time', 'language']
    list_filter = ['theater__city', 'theater', 'language', 'start_time']
    search_fields = ['movie__name', 'theater__name']
    date_hierarchy = 'start_time'


@admin.register(ShowSeat)
class ShowSeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'show', 'seat', 'status', 'price', 'locked_at']
    list_filter = ['status', 'show__start_time']
    search_fields = ['show__movie__name', 'seat__number']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email', 'phone']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone',)}),
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'show', 'amount', 'status', 'booking_time']
    list_filter = ['status', 'booking_time']
    search_fields = ['id', 'user__username', 'show__movie__name']
    date_hierarchy = 'booking_time'


@admin.register(TicketSeat)
class TicketSeatAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'show_seat', 'created_at']
    search_fields = ['ticket__id']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'amount', 'mode', 'status', 'timestamp']
    list_filter = ['status', 'mode', 'timestamp']
    search_fields = ['id', 'ticket__id', 'transaction_id']
    date_hierarchy = 'timestamp'


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'base_price', 'seat_type', 'is_active']
    list_filter = ['is_active', 'seat_type']
    search_fields = ['name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'valid_from', 'valid_until', 'is_active']
    list_filter = ['is_active', 'discount_type', 'valid_from']
    search_fields = ['code', 'description']
