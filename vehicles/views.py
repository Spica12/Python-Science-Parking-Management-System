from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle
from vehicles.forms import VehicleForm
from parking_service.models import ParkingSession
from vehicles.utils import get_total_parking_duration


# Create your views here.
@login_required(login_url="login")
def get_vehicles(request):
    vehicles = Vehicle.objects.filter(user=request.user)

    return render(
        request,
        "vehicles/vehicles.html",
        context={'vehicles': vehicles}
    )

@login_required(login_url="login")
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            return redirect("vehicles:vehicles")
    else:
        form = VehicleForm()

    return render(request, "vehicles/new_vehicle.html", {"form": form})

@login_required(login_url="login")
def del_vehicle(request, pk):
    # vehicle = get_object_or_404(Vehicle, pk=pk)
    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        vehicle = None

    if vehicle is not None:
        vehicle.delete()

    return redirect("vehicles:vehicles")


@login_required(login_url="login")
def detail_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    # try:
    #     vehicle = Vehicle.objects.get(pk=pk)
    # except Vehicle.DoesNotExist:
    #     vehicle = None

    parking_sessions = ParkingSession.objects.filter(vehicle=vehicle).all()

    # TODO Розрахувати загальний час паркування
    total_parking_duration = get_total_parking_duration(parking_sessions)

    context = {
        'vehicle': vehicle,
        'parking_sessions': parking_sessions,
        'total_parking_duration': total_parking_duration,
    }
    return render(request, "vehicles/detail_vehicle.html", context=context)
