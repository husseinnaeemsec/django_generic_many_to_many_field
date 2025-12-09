"""
Models for django_generic_many_to_many_field.
"""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GenericManyToManyRelation(models.Model):
    """
    Intermediate model for generic many-to-many relationships.
    
    This model stores the relationships between objects using
    Django's ContentType framework.
    """
    
    # Source object
    content_type_from = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='generic_relations_from'
    )
    object_id_from = models.PositiveIntegerField()
    content_object_from = GenericForeignKey('content_type_from', 'object_id_from')
    
    # Target object
    content_type_to = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='generic_relations_to'
    )
    object_id_to = models.PositiveIntegerField()
    content_object_to = GenericForeignKey('content_type_to', 'object_id_to')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Meta options for GenericManyToManyRelation."""
        unique_together = [
            ['content_type_from', 'object_id_from', 'content_type_to', 'object_id_to']
        ]
        indexes = [
            models.Index(fields=['content_type_from', 'object_id_from']),
            models.Index(fields=['content_type_to', 'object_id_to']),
        ]
        verbose_name = 'Generic Many-to-Many Relation'
        verbose_name_plural = 'Generic Many-to-Many Relations'
    
    def __str__(self):
        """String representation of the relation."""
        return f"{self.content_object_from} -> {self.content_object_to}"
