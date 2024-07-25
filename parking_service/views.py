from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from parking_service.models import ParkingSession


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
