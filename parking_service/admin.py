from django.contrib import admin
from .models import LicensePlate

@admin.register(LicensePlate)
class LicensePlateAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'detected_at')
    search_fields = ('plate_number',)
