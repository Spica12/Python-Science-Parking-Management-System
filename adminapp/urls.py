from django.urls import path

from django.contrib import admin

from adminapp import views

app_name = 'users'

urlpatterns = [
    path('', admin.site.urls),
    # path('panel/', views., name='admin_panel'),
]
