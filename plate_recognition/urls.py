from django.urls import path

from . import views

app_name = "plate_recognition"

urlpatterns = [
    path("upload/", views.upload_photo, name="upload"),
    path('confirm_plate_number/', views.confirm_plate_number, name='confirm_plate_number'),
]
