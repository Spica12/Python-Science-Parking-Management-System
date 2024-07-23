from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from parking_service.models import ParkingSession, StatusEnum
from vehicles.models import Vehicle
from parking_service.forms import UploadFileForm


# Create your views here.
def main_page(request):

    filename = ''
    manual_plate_number = ''
    plate_number = ''

    if request.method == "POST":
        # Приймання зображень від користувача
        # TODO Додати перевірку на розмір файлу (напркилад, не більше 8 мб)
        # TODO Додати перевірку на тип файлу (JPG, PNG та інші, якщо треба)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES.get("image")
            manual_plate_number = request.POST.get("manual_plate_number")

            # TODO Зробити логіку вибору між ручним номером та номером з фото. Поки що вибір ручного вводу номера
            if manual_plate_number:
                plate_number = manual_plate_number
            if uploaded_image:
                filename = uploaded_image.name

            # TODO Детекція номерного знаку
            # TODO Виявлення та виділення області з номерним знаком із зображень.
            # TODO Оптичне розпізнавання символів для ідентифікації тексту номерного знаку.

            # TODO Пошук номера авто у базі даних зареєстрованих транспортних засобів.
            # TODO Додати перевірку Якщо машина заблокована, то вивести інформацію, що засіб заблокований
            try:
                vehicle = Vehicle.objects.get(plate_number=plate_number)
                if vehicle.is_blocked:
                    context = {
                        'form': form,
                        'error_message': 'This vehicle is blocked.'
                    }
                    return render(request, 'main_page.html', context)
            except Vehicle.DoesNotExist:
                vehicle = Vehicle(plate_number=plate_number)
                vehicle.save()
                print('Create new vehicle')

            try:
                session = ParkingSession.objects.get(vehicle=vehicle, status=StatusEnum.PARKING)
                session.status = StatusEnum.FINISHED
                session.end_at = timezone.now()
                session.parking_duration = session.end_at - session.started_at
                session.save()
            except ParkingSession.DoesNotExist:
                session = ParkingSession(vehicle=vehicle, status=StatusEnum.PARKING)
                session.save()



            # TODO Повернути на головну сторінку: фото на якому буде виділено рамка з номером, номер засобу, дата та час
            # TODO Інформацію про стан паркування: Початок паркування, (Кінець паркування, Тривалість паркування, Вартість)
            context = {
                "filename": filename,
                'manual_plate_number': manual_plate_number,
                'status': session.status,
                'start_parking': session.started_at,
                'end_parking': session.end_at,
                'parking_duration': session.formatted_duration(),
            }

            return render(
                request,
                "parking_service/upload_result.html",
                context=context
            )

    else:
        form = UploadFileForm()

    return render(
        request,
        "parking_service/index.html",
        {"form": form}
    )
