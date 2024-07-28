from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from parking_service.models import ParkingSession, ParkingSpot, StatusParkingEnum
from finance.models import Tariff


def main_page(request):
    parking_spots = ParkingSpot.objects.all()
    paginator = Paginator(parking_spots, 24)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tariffs = Tariff.objects.all()

    context = {
        'parking_spots': page_obj,
        'tariffs': tariffs,
    }
    return render(request, 'parking_service/main_page.html', context)


def get_detail_parking_session(request, pk):
    # payment = get_object_or_404(Payment, pk=pk)
    try:
        parking_session = ParkingSession.objects.get(pk=pk)
        print(parking_session)
    except ParkingSession.DoesNotExist:
        return render(request, "vehicles/vehicles.html", context=context)

    context = {
        'session': parking_session,
    }
    return render(request, "parking_service/session_detail.html", context=context)
