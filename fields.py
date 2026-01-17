from django.db import models 
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from .widgets import DynamicObjectSelectWidget
from  django.utils.translation import gettext_lazy as _
import json


class GenericManyToManyField(models.TextField):
    
    def __init__(self,*args, **kwargs):
        self.content_type_field = kwargs.pop("content_type_field",None)
        
        super().__init__(*args, **kwargs)


    def to_python(self, value):
        """
        Converts the input value into a Python list.
        Handles inputs from forms (already a list of strings)
        and database (JSON string).
        """
        # Case 1: Value is already the desired Python type (a list)
        if isinstance(value, list):
            # The input from data.getlist() during form processing lands here first
            return value

        # Case 2: Handle None if the field is nullable
        if value is None:
            return None
            
        # Case 3: Value is a string (e.g., from database deserialization)
        # We attempt to decode it as JSON
        if isinstance(value, str):
            try:
                decoded_value = json.loads(value)
                print("Decoded data: ",decoded_value)
                if not isinstance(decoded_value, list):
                    raise ValidationError(_("This field must contain a list/array."))
                return decoded_value
            except json.JSONDecodeError:
                print(type(value),value)
                raise ValidationError(_("Invalid JSON format."))

        # Case 4: Any other unexpected input type
        raise ValidationError(_("Value must be a list or a valid JSON string representing a list."))


    def from_db_value(self, value, expression, connection):
        print("Getting value from database:", value)
        """
        Called when loading data from the database. 
        We rely on to_python to handle the actual type conversion safely.
        """
        # This calls to_python, which safely handles strings or None
        return self.to_python(value)

    def get_prep_value(self, value):
        print("Preparing value for database:", value)
        """
        Called when saving data to the database. Converts Python list to JSON string.
        """
        if value is None:
            return None
            
        if not isinstance(value, list):
             # Ensure we only dump lists, preventing the original error type
            raise ValidationError(_("Value stored in the database must be a list."))
            
        # ONLY dump if it is a list
        return json.dumps(value)


    def formfield(self, **kwargs):
        # Specify the custom form field to use
        from .config import CONTENTTYPE_MODEL_CHOICES_ENDPOINT
        defaults = {
            'widget':DynamicObjectSelectWidget(attrs={
                'content_type_field': self.content_type_field,
                'choices_endpoint':CONTENTTYPE_MODEL_CHOICES_ENDPOINT
            })
        }
        
        defaults.update(kwargs)
        
        return super().formfield(**defaults)
    

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        
        if not model_instance._meta.get_field(self.name).blank:
            if not isinstance(value, list):
                raise ValidationError("Must be a list.")
            
            if not all([str(v).isdigit() for v in value]):
                raise ValidationError("IDs must be integers.")
            
            value = [int(v) for v in value]

        if model_instance and self.content_type_field:
            content_type = getattr(model_instance, self.content_type_field)
            if content_type and isinstance(content_type, ContentType):
                model = content_type.model_class()
                for id in value:
                    if not model.objects.filter(id=id).exists():
                        raise ValidationError(
                            f"ID {id} does not exist in model {model.__name__}",
                            code='id_not_found',
                            params={"value":value}
                            )

class GenericManyToManyDescriptor:

    def __init__(self, content_type_field, id_field):
        self.content_type_field = content_type_field
        self.id_field = id_field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        content_type = getattr(instance, self.content_type_field)
        if not content_type or not isinstance(content_type, ContentType):
            return instance._meta.model.objects.none()

        ids = getattr(instance, self.id_field, [])
        if not isinstance(ids, list) or not ids:
            return instance._meta.model.objects.none()

        model = content_type.model_class()
        return model.objects.filter(id__in=ids)


