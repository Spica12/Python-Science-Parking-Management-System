from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from parking_service.models import Vehicle
from parking_service.forms import VehicleForm, UploadFileForm

# Create your views here.
def main_page(request):
    if request.method == "POST":

        # TODO Приймання зображень від користувача
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES.get("image")
            manual_plate_number = request.POST.get("manual_plate_number")
            if uploaded_image:
                filename = uploaded_image.name
                print(filename)
            if manual_plate_number:
                print(manual_plate_number)



            # TODO Детекція номерного знаку
            # TODO Виявлення та виділення області з номерним знаком із зображень.
            # TODO Оптичне розпізнавання символів для ідентифікації тексту номерного знаку.

            # TODO Пошук номера авто у базі даних зареєстрованих транспортних засобів.

            # TODO Повернути на головну сторінку: фото на якому буде виділено рамка з номером, номер засобу, дата та час
            # TODO Інформацію про стан паркування: Початок паркування, (Кінець паркування, Тривалість паркування, Вартість)
            # TODO Якщо машина заблокована, то вивести інформацію, що засіб заблокований

            return redirect("parking_service:main")


    else:
        form = UploadFileForm()

    return render(
        request,
        "parking_service/index.html",
        {"form": form}
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
            vehicle.user = request.user
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
