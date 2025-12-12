"""
Management command to seed the database with sample data
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from bookmyshow.booking.models import (
    City, Theater, Screen, Seat, Movie, Show, ShowSeat,
    SeatType, PricingRule
)


class Command(BaseCommand):
    help = 'Seed the database with sample data for BookMyShow'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data seeding...')

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        ShowSeat.objects.all().delete()
        Show.objects.all().delete()
        Movie.objects.all().delete()
        Seat.objects.all().delete()
        Screen.objects.all().delete()
        Theater.objects.all().delete()
        City.objects.all().delete()
        PricingRule.objects.all().delete()

        # Create cities
        self.stdout.write('Creating cities...')
        mumbai = City.objects.create(id='mumbai', name='Mumbai')
        delhi = City.objects.create(id='delhi', name='Delhi')
        bangalore = City.objects.create(id='bangalore', name='Bangalore')

        # Create theaters
        self.stdout.write('Creating theaters...')
        pvr_mumbai = Theater.objects.create(
            id='pvr-mumbai-1',
            name='PVR Juhu',
            address='Juhu Tara Road, Mumbai',
            city=mumbai
        )

        inox_mumbai = Theater.objects.create(
            id='inox-mumbai-1',
            name='INOX R-City',
            address='Ghatkopar, Mumbai',
            city=mumbai
        )

        pvr_delhi = Theater.objects.create(
            id='pvr-delhi-1',
            name='PVR Saket',
            address='Saket, New Delhi',
            city=delhi
        )

        # Create screens and seats
        self.stdout.write('Creating screens and seats...')
        for theater in [pvr_mumbai, inox_mumbai, pvr_delhi]:
            for screen_num in range(1, 4):  # 3 screens per theater
                screen = Screen.objects.create(
                    id=f'{theater.id}-screen-{screen_num}',
                    name=f'Audi {screen_num}',
                    theater=theater
                )

                # Create seats (A1-A10: Gold, B1-B10: Platinum, C1-C5: Diamond)
                seat_config = [
                    ('A', 10, SeatType.GOLD),
                    ('B', 10, SeatType.PLATINUM),
                    ('C', 5, SeatType.DIAMOND)
                ]

                for row, count, seat_type in seat_config:
                    for num in range(1, count + 1):
                        Seat.objects.create(
                            id=f'{screen.id}-{row}{num}',
                            number=f'{row}{num}',
                            seat_type=seat_type,
                            screen=screen
                        )

        # Create movies
        self.stdout.write('Creating movies...')
        movies_data = [
            {
                'id': 'movie-1',
                'name': 'Avengers: Endgame',
                'rating': 8.5,
                'category': 'Action',
                'languages': ['English', 'Hindi'],
                'duration': 181,
                'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins.'
            },
            {
                'id': 'movie-2',
                'name': 'Inception',
                'rating': 8.8,
                'category': 'Sci-Fi',
                'languages': ['English'],
                'duration': 148,
                'description': 'A thief who steals corporate secrets through dream-sharing technology.'
            },
            {
                'id': 'movie-3',
                'name': 'The Dark Knight',
                'rating': 9.0,
                'category': 'Action',
                'languages': ['English', 'Hindi'],
                'duration': 152,
                'description': 'When the menace known as the Joker wreaks havoc on Gotham.'
            },
            {
                'id': 'movie-4',
                'name': 'Interstellar',
                'rating': 8.6,
                'category': 'Sci-Fi',
                'languages': ['English'],
                'duration': 169,
                'description': 'A team of explorers travel through a wormhole in space.'
            }
        ]

        movies = []
        for movie_data in movies_data:
            movie = Movie.objects.create(**movie_data)
            movies.append(movie)

        # Create pricing rules
        self.stdout.write('Creating pricing rules...')
        PricingRule.objects.create(
            id='RULE-GOLD',
            name='Gold Seat Base Price',
            base_price=Decimal('200.00'),
            seat_type=SeatType.GOLD,
            seat_multiplier=Decimal('1.0')
        )
        PricingRule.objects.create(
            id='RULE-PLATINUM',
            name='Platinum Seat Pricing',
            base_price=Decimal('200.00'),
            seat_type=SeatType.PLATINUM,
            seat_multiplier=Decimal('1.3')
        )
        PricingRule.objects.create(
            id='RULE-DIAMOND',
            name='Diamond Seat Pricing',
            base_price=Decimal('200.00'),
            seat_type=SeatType.DIAMOND,
            seat_multiplier=Decimal('1.5')
        )

        # Create shows
        self.stdout.write('Creating shows...')
        show_count = 0

        for theater in Theater.objects.all():
            for screen in theater.screens.all():
                # 2 shows per screen
                for show_num in range(2):
                    movie = movies[show_count % len(movies)]

                    # Schedule shows for tomorrow
                    base_time = timezone.now() + timedelta(days=1)
                    if show_num == 0:
                        start_time = base_time.replace(hour=14, minute=0)  # 2 PM
                    else:
                        start_time = base_time.replace(hour=18, minute=30)  # 6:30 PM

                    show = Show.objects.create(
                        id=f'show-{show_count + 1}',
                        movie=movie,
                        screen=screen,
                        theater=theater,
                        start_time=start_time,
                        duration=movie.duration,
                        language=movie.languages[0]
                    )

                    # Create ShowSeats
                    for seat in screen.seats.all():
                        # Calculate price based on seat type
                        base_prices = {
                            SeatType.GOLD: Decimal('200.00'),
                            SeatType.PLATINUM: Decimal('260.00'),
                            SeatType.DIAMOND: Decimal('300.00')
                        }

                        price = base_prices.get(seat.seat_type, Decimal('200.00'))

                        ShowSeat.objects.create(
                            id=f'{show.id}-{seat.id}',
                            show=show,
                            seat=seat,
                            price=price,
                            status='AVAILABLE'
                        )

                    show_count += 1

        # Print summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'Cities created: {City.objects.count()}')
        self.stdout.write(f'Theaters created: {Theater.objects.count()}')
        self.stdout.write(f'Screens created: {Screen.objects.count()}')
        self.stdout.write(f'Seats created: {Seat.objects.count()}')
        self.stdout.write(f'Movies created: {Movie.objects.count()}')
        self.stdout.write(f'Shows created: {Show.objects.count()}')
        self.stdout.write(f'ShowSeats created: {ShowSeat.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. Access admin panel: http://localhost:8000/admin/')
        self.stdout.write('2. Browse APIs: http://localhost:8000/api/')
        self.stdout.write('3. Search movies: http://localhost:8000/api/movies/')
        self.stdout.write('4. View shows: http://localhost:8000/api/shows/')
