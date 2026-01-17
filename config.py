from django.urls import reverse_lazy
APP_NAME = 'django_generic_many_to_many_field'
CONTENTTYPE_MODEL_CHOICES_VIEW_NAME = 'get_contenttype_model_choices'
CONTENTTYPE_MODEL_CHOICES_ENDPOINT = reverse_lazy(f"{APP_NAME}:{CONTENTTYPE_MODEL_CHOICES_VIEW_NAME}")