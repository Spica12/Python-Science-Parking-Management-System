from django.urls import path

from vehicles import views

app_name = "vehicles"

urlpatterns = [
    path("", views.get_vehicles, name="vehicles"),
    path("<int:pk>/delete/", views.del_vehicle, name="del_vehicle"),
    path("<int:pk>/detail/", views.detail_vehicle, name="detail_vehicle"),
    path("new", views.add_vehicle, name="new_vehicle"),
]
