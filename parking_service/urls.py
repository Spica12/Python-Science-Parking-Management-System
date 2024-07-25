from django.urls import path

from . import views

app_name = "parking_service"

urlpatterns = [
    path("", views.main_page, name="main"),
    path("session/<int:pk>/detail/", views.get_detail_parking_session, name="detail_session"),
]
