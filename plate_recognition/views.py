from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from finance.models import Payment
from parking_service.models import ParkingSession, StatusParkingEnum
from vehicles.models import Vehicle, StatusVehicleEnum
from plate_recognition.forms import UploadFileForm, ConfirmPlateForm
from plate_recognition.service_predict import image_plate_recognition


# Create your views here.
def upload_photo(request):

    filename = ''
    manual_plate_number = ''
    plate_number = ''

    if request.method == "POST":
        # Приймання зображень від користувача
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # uploaded_image = request.FILES.get("image")
            # manual_plate_number = request.POST.get("manual_plate_number")
            uploaded_image = form.cleaned_data.get('image')
            manual_plate_number = form.cleaned_data.get('manual_plate_number')

            request.session['predicted_plate_number'] = ''
            request.session['confirmed_plate_number'] = ''

            # TODO Зробити логіку вибору між ручним номером та номером з фото. Поки що вибір ручного вводу номера
            if not uploaded_image and not manual_plate_number:
                context = {
                    'form': form,
                    'error_message': 'You need enter manual plate number or upload image.'
                }
                return render(request, "plate_recognition/photo_upload.html", context)
            if uploaded_image and not manual_plate_number:
                filename = uploaded_image.name
                # Детекція номерного знаку
                # Виявлення та виділення області з номерним знаком із зображень.
                # Оптичне розпізнавання символів для ідентифікації тексту номерного знаку.
                img_predict = image_plate_recognition.predict_plate(file=uploaded_image)

                request.session['predicted_plate_number'] = img_predict.get('num_vehicle_str')
                request.session['num_img'] = img_predict.get('num_img')
                request.session['filename'] = uploaded_image.name

                # return redirect('plate_recognition:confirm_plate_number')
            if manual_plate_number:
                request.session['confirmed_plate_number'] = manual_plate_number

            return redirect('plate_recognition:confirm_plate_number')

    else:
        form = UploadFileForm()

    return render(
        request,
        "plate_recognition/photo_upload.html",
        {"form": form}
    )


def confirm_plate_number(request):
    print('confirm start')
    predicted_plate_number = request.session.get('predicted_plate_number', '')
    confirmed_plate_number = request.session.get('confirmed_plate_number', '')
    manual_plate_number = request.session.get('confirmed_plate_number', '')
    num_img = request.session.get('num_img', '')
    filename = request.session.get('filename', '')

    if request.method == 'POST' and not confirmed_plate_number:
        print('confirm post')
        form = ConfirmPlateForm(request.POST)
        if form.is_valid():
            print('confirm form is valid')
            confirmed_plate_number = form.cleaned_data.get('confirm_plate_number')
            request.session.pop('filename', None)
            # request.session.pop('confirmed_plate_number', None)
            # request.session.pop('predicted_plate_number', None)
            request.session.pop('num_img', None)

    elif request.method == 'GET' and not confirmed_plate_number:
        form = ConfirmPlateForm(initial={'confirm_plate_number': predicted_plate_number})

        context = {
            'form': form,
            'predict_plate_number': predicted_plate_number,
            'num_img': num_img,
        }

        return render(request, 'plate_recognition/confirm_plate_number.html', context=context)

    print('c', confirmed_plate_number)
    if confirmed_plate_number:
        print('confirmed_plate_number')
        # TODO Пошук номера авто у базі даних зареєстрованих транспортних засобів.
        # TODO Додати перевірку Якщо машина заблокована, то вивести інформацію, що засіб заблокований

        try:
            vehicle = Vehicle.objects.get(plate_number=confirmed_plate_number)
            if vehicle.status == StatusVehicleEnum.BLOCKED.name:
                context = {
                    'form': form,
                    'error_message': 'This vehicle is blocked.'
                }
                return render(request, 'main_page.html', context)
        except Vehicle.DoesNotExist:
            vehicle = Vehicle(plate_number=confirmed_plate_number, status = StatusVehicleEnum.UNREGISTERED.name)
            vehicle.save()

        try:
            session = ParkingSession.objects.get(vehicle=vehicle, status=StatusParkingEnum.ACTIVE.name)
            session.status = StatusParkingEnum.FINISHED.name
            session.end_at = timezone.now()
            payment = Payment(parking_session_pk=session, amount=0)
            session.save()
            payment.save()

        except ParkingSession.DoesNotExist:
            session = ParkingSession(vehicle=vehicle, status=StatusParkingEnum.ACTIVE.name)
            session.save()

    # TODO Повернути на головну сторінку: фото на якому буде виділено рамка з номером, номер засобу, дата та час
    # TODO Інформацію про стан паркування: Початок паркування, (Кінець паркування, Тривалість паркування, Вартість)

    context = {
        'filename': filename,
        'manual_plate_number': manual_plate_number,
        'predict_plate_number': predicted_plate_number,
        'num_img': num_img,
        'session': session,
    }

    return render(
        request,
        "plate_recognition/photo_upload_result.html",
        context=context
    )
