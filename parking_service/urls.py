from django.urls import path

from . import views

app_name = "parking_service"

urlpatterns = [
    path("", views.main_page, name="main"),
]
