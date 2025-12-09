"""
Generic many-to-many field implementation.
"""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class GenericManyToManyField(GenericRelation):
    """
    A field that provides a generic many-to-many relationship.
    
    This field allows models to have many-to-many relationships with
    any model using Django's ContentType framework.
    
    Usage:
        from django_generic_many_to_many_field.fields import GenericManyToManyField
        
        class MyModel(models.Model):
            related_items = GenericManyToManyField()
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the generic many-to-many field."""
        super().__init__(*args, **kwargs)
