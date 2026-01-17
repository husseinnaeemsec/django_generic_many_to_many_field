# widgets.py
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
import json

class DynamicObjectSelectWidget(forms.Textarea):
    template_name = "dgm2mf/widgets/dynamic_json_field.html"

    def value_from_datadict(self, data, files, name):
        try:
            value = data.getlist(name)
        except:
            value = data.get(name)

        if not isinstance(value, list):
            raise ValidationError("Value must be a list.")
        
        if not all(str(v).isdigit() for v in value):
            raise ValidationError("All values must be digits.")
        
        value = [int(v) for v in  value ]

        
        return value

    class Media:
        js = ["dgm2mf/js/dynamic-m2m.js"]
