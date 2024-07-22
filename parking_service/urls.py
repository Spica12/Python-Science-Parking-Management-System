from django.urls import path

from . import views

app_name = "parking_service"

urlpatterns = [
    path("", views.main_page, name="main"),
    path("vehicles/", views.get_vehicles, name="vehicles"),
    path("vehicles/<int:pk>/delete/", views.del_vehicle, name="del_vehicle"),
    path("vehicles/new", views.add_vehicle, name="new_vehicle"),
]
