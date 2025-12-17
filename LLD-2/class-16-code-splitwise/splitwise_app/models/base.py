from django.db import models


class BaseModel(models.Model):
    """
    Base model for all models with audit fields.
    All models should inherit from this to get created_at and updated_at.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
