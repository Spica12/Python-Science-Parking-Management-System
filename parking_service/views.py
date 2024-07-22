from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from parking_service.models import Vehicle
from parking_service.forms import VehicleForm

# Create your views here.
def main_page(request):

    return render(
        request,
        "parking_service/index.html",
    )

@login_required(login_url="login")
def get_vehicles(request):
    vehicles = Vehicle.objects.filter(user=request.user)

    return render(
        request,
        "parking_service/vehicles.html",
        context={'vehicles': vehicles}
    )

@login_required(login_url="login")
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.save()
            return redirect("parking_service:vehicles")
    else:
        form = VehicleForm()

    return render(request, "parking_service/new_vehicle.html", {"form": form})

@login_required(login_url="login")
def del_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if vehicle is not None:
        vehicle.delete()

    return redirect("parking_service:vehicles")
