from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from adminapp.decorators import admin_or_operator_required
from vehicles.models import Vehicle
from vehicles.forms import VehicleForm
from parking_service.models import ParkingSession, StatusParkingEnum
from vehicles.utils import get_total_parking_duration
from users.decorators import user_is_verified

# @user_is_verified (Replace login_required)
@login_required(login_url="login")
def get_vehicles(request):
    vehicles = Vehicle.objects.filter(user=request.user)

    paginator = Paginator(vehicles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, "vehicles/vehicles.html", context=context)

# @admin_or_operator_required
# Треба змінити назву функції, тому-що через те що дві однакових
# не працює сторінка транспортних засобів користувача
# 
def get_vehicles(request):
    vehicles = Vehicle.objects.filter()

    paginator = Paginator(vehicles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, "vehicles/vehicles.html", context=context)

# @user_is_verified (Replace login_required)
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

# @user_is_verified (Replace login_required)
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

# @user_is_verified (Replace login_required)
@login_required(login_url="login")
def detail_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    # try:
    #     vehicle = Vehicle.objects.get(pk=pk)
    # except Vehicle.DoesNotExist:
    #     vehicle = None

    # TODO Додати фільтер по FINISHED status
    parking_sessions = ParkingSession.objects.filter(vehicle=vehicle).all().order_by("-started_at")

    paginator = Paginator(parking_sessions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_parking_duration = get_total_parking_duration(parking_sessions)

    context = {
        'vehicle': vehicle,
        'page_obj': page_obj,
        'total_parking_duration': total_parking_duration,
    }
    return render(request, "vehicles/detail_vehicle.html", context=context)
