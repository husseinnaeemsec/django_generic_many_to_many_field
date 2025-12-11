"""
Generic many-to-many field implementation.
"""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.contenttypes.models import ContentType

class GenericManyToManyManager:
    
    def __init__(self, instance, ct_field, id_field):
        self.instance = instance
        self.ct_field = ct_field
        self.id_field = id_field
        self.ct = getattr(self.instance,self.ct_field)
        self.ids = getattr(self.instance,self.id_field) or []
        self.ct_model = self.ct.model_class()
        
    
    def all(self):
        if not self.ct or not self.ids:
            return []
        model = self.ct.model_class()
        return list(model.objects.filter(id__in=self.ids))
    
    def remove(self,id):
        if id in self.ids:
            self.ids.remove(id)
            setattr(self.instance, self.id_field, self.ids)
            getattr(self.instance,'save')(updated_fields=[self.id_field])
    def add(self,id):
        if id not in self.ids:
            self.ids.append(id)
            setattr(self.instance, self.id_field, self.ids)
            getattr(self.instance,'save')(updated_fields=[self.id_field])
    
    def set(self,ids):
        if not isinstance(ids, (list, tuple)) or not all(isinstance(id,int) for id in ids):
            raise TypeError(f"All values must be instance of int for ids.")
        
        self.ids = ids
        setattr(self.instance, self.id_field, self.ids)
        getattr(self.instance,'save')(updated_fields=[self.id_field])

class GenericManyToManyDescriptor:

    def __init__(self, field_name, ct_field, id_field):
        self.field_name = field_name          # JSONField
        self.ct_field = ct_field              # content type
        self.id_field = id_field              # list of object IDs

    def __get__(self, instance, owner):
        if not instance:
            return None
        self.instance = instance
        self.owner = owner
        return self

    

    @property
    def objects(self):
        
        return GenericManyToManyManager(
            self.instance,
            self.ct_field,
            self.id_field,
        )

    def __set__(self, instance, value):
        """
        value يمكن أن يكون:
        - object
        - list of objects
        - list of IDs
        """

        if not value:
            setattr(instance, self.id_field, [])
            setattr(instance, self.ct_field, None)
            return

        # ⚠️ إذا single object → حوّل إلى list
        if not isinstance(value, (list, tuple)):
            value = [value]

        # جلب IDs
        ids = [obj.id if hasattr(obj, "id") else obj for obj in value]

        # جلب content type من أول object
        first_obj = value[0]
        model = first_obj.__class__
        ct = ContentType.objects.get_for_model(model)

        setattr(instance, self.ct_field, ct)
        setattr(instance, self.id_field, ids)

    @classmethod
    def contribute_to_class(cls, model, name):
        # This is important
        setattr(model, name, cls(
            field_name=name,
            ct_field=f"{name}_content_type",
            id_field=f"{name}_ids"
        ))

