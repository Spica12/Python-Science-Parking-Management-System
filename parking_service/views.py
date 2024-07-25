from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from finance.models import Payment
from parking_service.models import ParkingSession, StatusParkingEnum
from vehicles.models import Vehicle, StatusVehicleEnum
from parking_service.forms import UploadFileForm


# Create your views here.
def main_page(request):


    return render(request,"parking_service/index.html",)


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
