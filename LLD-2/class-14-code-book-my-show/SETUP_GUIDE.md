# Setup Guide - BookMyShow Project

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Step-by-Step Setup

### 1. Navigate to Project Directory

```bash
cd /path/to/class-14-code-book-my-show
```

### 2. Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.7
- Django REST Framework 3.14.0
- Django Filter 23.3

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the database tables.

### 5. Create Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

Enter:
- Username: admin (or your choice)
- Email: admin@example.com
- Password: (choose a secure password)

### 6. Start Development Server

```bash
python manage.py runserver
```

The server will start at: http://localhost:8000

### 7. Verify Installation

Open your browser and visit:

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/api/health/

## Adding Sample Data

### Option 1: Using Management Command (Easiest!) ⭐

Run this single command to populate the database with sample data:

```bash
python manage.py seed_data
```

This will create:
- 3 cities (Mumbai, Delhi, Bangalore)
- 3 theaters with 3 screens each
- 25 seats per screen (different seat types)
- 4 movies
- Multiple shows scheduled for tomorrow
- ShowSeats for all shows

### Option 2: Via Django Admin

1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Add data in this order:
   - Cities
   - Theaters
   - Screens
   - Seats
   - Movies
   - Shows
   - ShowSeats (created automatically when show is created)

### Option 3: Via Django Shell

```bash
python manage.py shell
```

Then run:

```python
from bookmyshow.booking.models import *
from django.utils import timezone
from datetime import timedelta
import uuid

# Create City
mumbai = City.objects.create(id='mumbai', name='Mumbai')

# Create Theater
pvr = Theater.objects.create(
    id='pvr-mumbai-1',
    name='PVR Juhu',
    address='Juhu Tara Road, Mumbai',
    city=mumbai
)

# Create Screen
screen = Screen.objects.create(
    id='screen-1',
    name='Audi 1',
    theater=pvr
)

# Create Seats
seat_types = ['GOLD', 'GOLD', 'PLATINUM', 'PLATINUM', 'DIAMOND']
for i, seat_type in enumerate(seat_types, 1):
    Seat.objects.create(
        id=f'seat-{i}',
        number=f'A{i}',
        seat_type=seat_type,
        screen=screen
    )

# Create Movie
movie = Movie.objects.create(
    id='movie-1',
    name='Avengers: Endgame',
    rating=8.5,
    category='Action',
    languages=['English', 'Hindi'],
    duration=181,
    description='After the devastating events...'
)

# Create Show
show_time = timezone.now() + timedelta(days=1, hours=6)  # Tomorrow 6 PM
show = Show.objects.create(
    id='show-1',
    movie=movie,
    screen=screen,
    theater=pvr,
    start_time=show_time,
    duration=181,
    language='English'
)

# Create ShowSeats
for seat in screen.seats.all():
    base_price = {
        'GOLD': 200,
        'DIAMOND': 300,
        'PLATINUM': 350
    }[seat.seat_type]

    ShowSeat.objects.create(
        id=f'showseat-{seat.id}',
        show=show,
        seat=seat,
        price=base_price,
        status='AVAILABLE'
    )

print("Sample data created successfully!")
```

## Testing the APIs

### Using curl

```bash
# Health Check
curl http://localhost:8000/api/health/

# List Cities
curl http://localhost:8000/api/cities/

# List Movies
curl http://localhost:8000/api/movies/

# Get Show Details
curl http://localhost:8000/api/shows/show-1/
```

### Using Postman

1. Download Postman: https://www.postman.com/downloads/
2. Import the API endpoints
3. Test the APIs

## Troubleshooting

### Error: "No module named 'django'"

**Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "django.db.utils.OperationalError: no such table"

**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Error: "Port 8000 is already in use"

**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```

Or kill the process using port 8000.

### Error: "CSRF verification failed"

**Solution**: For testing, you can disable CSRF for specific endpoints or use session authentication. In production, include CSRF token.

## Next Steps

1. ✅ Read `README.md` for project overview
2. ✅ Explore `bookmyshow/guides/` for learning materials
3. ✅ Start with `guides/01_MODELS_AND_RELATIONSHIPS.md`
4. ✅ Experiment with the APIs
5. ✅ Read concurrency control guide (most important!)
6. ✅ Practice explaining the design

## Useful Commands

```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Run tests (if you add them)
python manage.py test

# Check for issues
python manage.py check
```

## Project Structure Quick Reference

```
bookmyshow/
├── bookmyshow/booking/
│   ├── models.py              # Database models
│   ├── serializers.py         # API serializers
│   ├── views.py               # API controllers
│   ├── urls.py                # API routes
│   └── services/              # Business logic
│       ├── booking_service_pessimistic.py
│       ├── booking_service_optimistic.py
│       └── booking_service_thread.py
│
└── bookmyshow/guides/         # Learning materials
    ├── 01_MODELS_AND_RELATIONSHIPS.md
    ├── 02_SERIALIZERS.md
    ├── 03_CONCURRENCY_CONTROL.md    ⭐ Most important!
    ├── 04_ARCHITECTURE_AND_DATA_FLOW.md
    ├── 05_API_DOCUMENTATION.md
    └── 06_INTERVIEW_GOTCHAS.md
```

## Getting Help

- Read the guides in `bookmyshow/guides/`
- Check Django documentation: https://docs.djangoproject.com/
- Check DRF documentation: https://www.django-rest-framework.org/

Happy learning! 🚀
