from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('adminapp.urls', namespace='adminapp')),
    path('', include('parking_service.urls', namespace='parking')),
    path('users/', include('users.urls', namespace='users')),
    path('vehicles/', include('vehicles.urls', namespace='vehicles')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
