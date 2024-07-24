from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path("payments_list/", views.get_payments_list_by_user, name="payments_list_by_user"),
]
