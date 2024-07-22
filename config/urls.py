from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parking_service.urls', namespace='parking')),
    path('users/', include('users.urls', namespace='users')),
]
