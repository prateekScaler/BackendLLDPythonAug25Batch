"""
Base Service Layer
Following Service-Oriented Architecture for better separation of concerns

Interview Notes:
- Services contain business logic
- Keep views thin, services fat
- Makes testing easier (can test services without HTTP layer)
- Reusable across different interfaces (REST API, GraphQL, etc.)
"""


class BaseService:
    """
    Base service class with common functionality
    Interview Tip: Use base classes to avoid code duplication
    """

    @staticmethod
    def validate_required_fields(data, required_fields):
        """Validate that all required fields are present"""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    @staticmethod
    def safe_get_or_none(model, **kwargs):
        """
        Safely get object or return None
        Interview Tip: Avoid try-except for every query
        """
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None
        except model.MultipleObjectsReturned:
            return model.objects.filter(**kwargs).first()
