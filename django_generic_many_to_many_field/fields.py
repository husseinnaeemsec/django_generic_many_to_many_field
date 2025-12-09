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
    
    Note:
        This is a specialized version of GenericRelation configured for
        many-to-many relationships through the GenericManyToManyRelation model.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the generic many-to-many field.
        
        Sets up the relationship to use the GenericManyToManyRelation model
        as the intermediary table.
        """
        # Set default related model if not specified
        if 'to' not in kwargs:
            from .models import GenericManyToManyRelation
            kwargs['to'] = GenericManyToManyRelation
        
        # Configure content type fields
        if 'content_type_field' not in kwargs:
            kwargs['content_type_field'] = 'content_type_from'
        if 'object_id_field' not in kwargs:
            kwargs['object_id_field'] = 'object_id_from'
        
        super().__init__(*args, **kwargs)
    
    def contribute_to_class(self, cls, name, **kwargs):
        """Contribute the field to the model class."""
        super().contribute_to_class(cls, name, **kwargs)
        
        # Add helper methods to the model
        setattr(cls, f'get_{name}_count', self._make_get_count_method(name))
    
    def _make_get_count_method(self, field_name):
        """Create a method to get the count of related objects."""
        def get_count(instance):
            """Get the count of related objects."""
            return getattr(instance, field_name).count()
        
        get_count.__name__ = f'get_{field_name}_count'
        get_count.__doc__ = f'Get the count of {field_name}.'
        return get_count

