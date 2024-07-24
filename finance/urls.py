from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path("payments/list/", views.get_payments_list_by_user, name="payments_list_by_user"),
    path("tariffs/add", views.add_tariff, name="tariff_add"),
    path("tariffs/list/", views.get_tariffs_list, name="tariffs_list"),
    path("tariffs/<int:pk>/delete/", views.delete_tariff, name="tariff_delete"),
]
