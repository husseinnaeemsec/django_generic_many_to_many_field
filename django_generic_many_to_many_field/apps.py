"""
Django app configuration for django_generic_many_to_many_field.
"""

from django.apps import AppConfig


class DjangoGenericManyToManyFieldConfig(AppConfig):
    """Configuration for the django_generic_many_to_many_field app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_generic_many_to_many_field'
    verbose_name = 'Django Generic Many-to-Many Field'
