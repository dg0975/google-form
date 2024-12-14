from rest_framework import routers
from django.urls import path

from form_builder import views

app_name = 'form_builder'

router = routers.DefaultRouter()

urlpatterns = [
    path("samples/<int:form_id>/", views.submit_form_response, name="submit_form_response"),
    path("results/<int:form_id>/", views.view_responses, name="view_responses"),
]

