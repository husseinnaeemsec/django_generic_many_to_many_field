"""
Django admin configuration for django_generic_many_to_many_field.
"""

from django.contrib import admin
from .models import GenericManyToManyRelation


@admin.register(GenericManyToManyRelation)
class GenericManyToManyRelationAdmin(admin.ModelAdmin):
    """Admin interface for GenericManyToManyRelation model."""
    
    list_display = [
        'id',
        'content_type_from',
        'object_id_from',
        'content_type_to',
        'object_id_to',
        'created_at',
    ]
    list_filter = ['content_type_from', 'content_type_to', 'created_at']
    search_fields = ['object_id_from', 'object_id_to']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
