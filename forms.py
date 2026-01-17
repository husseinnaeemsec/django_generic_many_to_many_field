from django import forms
from .widgets import DynamicObjectSelectWidget

class GenericManyToManyJSONFormField(forms.JSONField):
    def __init__(self, *args, **kwargs):
        # Set the custom widget as the default
        kwargs.setdefault('widget', DynamicObjectSelectWidget(
            attrs={
                'content_type_field': kwargs.pop('content_type_field')
            }
        ))
        super().__init__(*args, **kwargs)