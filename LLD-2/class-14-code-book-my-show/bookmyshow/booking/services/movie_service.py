"""
Movie Service
Handles movie search and filtering logic

Interview Points:
- Demonstrates complex querying with Django ORM
- Query optimization with select_related/prefetch_related
- Filtering and searching patterns
"""
from django.db.models import Q, Count, Prefetch
from django.utils import timezone

from ..models import Movie, Show, City, Theater
from .base_service import BaseService


class MovieService(BaseService):
    """
    Service for movie-related operations

    Interview Note: Separation of concerns - queries are in service, not views
    """

    @staticmethod
    def search_movies(query, city_id=None, category=None, language=None, min_rating=None):
        """
        Search movies with filters

        Interview Points:
        1. Q objects for complex queries (OR conditions)
        2. Filter chaining for AND conditions
        3. Query optimization

        Example:
        Search "Avengers" in Mumbai, Action category, English, rating > 7
        """
        movies = Movie.objects.all()

        # Text search - Interview Note: Use Q for OR conditions
        if query:
            movies = movies.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )

        # Filter by category
        if category:
            movies = movies.filter(category__iexact=category)

        # Filter by language - Interview Note: JSONField querying
        if language:
            movies = movies.filter(languages__contains=[language])

        # Filter by rating
        if min_rating:
            movies = movies.filter(rating__gte=min_rating)

        # Filter by city - Interview Note: Join through multiple tables
        if city_id:
            movies = movies.filter(
                shows__theater__city_id=city_id,
                shows__start_time__gte=timezone.now()
            ).distinct()

        # Annotate with show count - Interview Note: Aggregations
        movies = movies.annotate(
            upcoming_shows_count=Count(
                'shows',
                filter=Q(shows__start_time__gte=timezone.now())
            )
        )

        return movies.order_by('-rating', 'name')

    @staticmethod
    def get_movie_shows(movie_id, city_id=None, date=None):
        """
        Get all shows for a movie

        Interview Note: Complex filtering with date ranges
        """
        shows = Show.objects.filter(
            movie_id=movie_id,
            start_time__gte=timezone.now()
        ).select_related(
            'movie', 'theater', 'theater__city', 'screen'
        )

        if city_id:
            shows = shows.filter(theater__city_id=city_id)

        if date:
            # Filter by date - Interview Note: Date range filtering
            from datetime import datetime, timedelta
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = start_of_day + timedelta(days=1)
            shows = shows.filter(
                start_time__gte=start_of_day,
                start_time__lt=end_of_day
            )

        return shows.order_by('start_time')

    @staticmethod
    def get_theaters_for_movie(movie_id, city_id):
        """
        Get all theaters showing a movie in a city

        Interview Note: Distinct theaters with show count
        """
        theaters = Theater.objects.filter(
            shows__movie_id=movie_id,
            shows__start_time__gte=timezone.now(),
            city_id=city_id
        ).annotate(
            shows_count=Count('shows')
        ).distinct().order_by('name')

        return theaters

    @staticmethod
    def get_available_filters(city_id=None):
        """
        Get available filter options (categories, languages, etc.)

        Interview Note: Dynamic filter generation for UI
        """
        movies = Movie.objects.filter(
            shows__start_time__gte=timezone.now()
        )

        if city_id:
            movies = movies.filter(shows__theater__city_id=city_id)

        movies = movies.distinct()

        # Get unique categories
        categories = movies.values_list('category', flat=True).distinct()

        # Get unique languages - Interview Note: JSONField aggregation is tricky
        languages = set()
        for movie in movies:
            languages.update(movie.languages)

        return {
            'categories': sorted(categories),
            'languages': sorted(languages),
            'min_rating': movies.order_by('rating').first().rating if movies.exists() else 0,
            'max_rating': movies.order_by('-rating').first().rating if movies.exists() else 10,
        }
