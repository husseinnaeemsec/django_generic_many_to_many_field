from django.urls import path
from .views import get_contenttype_model_choices
from . import config

app_name= config.APP_NAME

urlpatterns = [
    path("get_contenttype_model_choices/", get_contenttype_model_choices, name=config.CONTENTTYPE_MODEL_CHOICES_VIEW_NAME)
]