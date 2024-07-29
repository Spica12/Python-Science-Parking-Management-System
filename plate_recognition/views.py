from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from finance.models import Account, Payment, TypePaymentEnum
from parking_service.models import ParkingSession, StatusParkingEnum
from vehicles.models import Vehicle, StatusVehicleEnum
from plate_recognition.forms import UploadFileForm, ConfirmPlateForm
from plate_recognition.service_predict import image_plate_recognition
from parking_service.models import ParkingSpot


# Create your views here.
def upload_photo(request):

    filename = ''
    manual_plate_number = ''
    plate_number = ''

    request.session['predicted_plate_number'] = ''
    request.session['confirmed_plate_number'] = ''
    request.session['num_img'] = ''
    request.session['filename'] = ''

    if request.method == "POST":
        # Приймання зображень від користувача
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # uploaded_image = request.FILES.get("image")
            # manual_plate_number = request.POST.get("manual_plate_number")
            uploaded_image = form.cleaned_data.get('image')
            manual_plate_number = form.cleaned_data.get('manual_plate_number')

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
    predicted_plate_number = request.session.get('predicted_plate_number', '')
    confirmed_plate_number = request.session.get('confirmed_plate_number', '')
    manual_plate_number = request.session.get('confirmed_plate_number', '')
    num_img = request.session.get('num_img', '')
    filename = request.session.get('filename', '')

    if request.method == 'POST' and not confirmed_plate_number:
        form = ConfirmPlateForm(request.POST)
        if form.is_valid():
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

    if confirmed_plate_number:
        # TODO Пошук номера авто у базі даних зареєстрованих транспортних засобів.
        # TODO Додати перевірку Якщо машина заблокована, то вивести інформацію, що засіб заблокований

        form = None

        try:
            vehicle = Vehicle.objects.get(plate_number=confirmed_plate_number)
            if vehicle.status == StatusVehicleEnum.BLOCKED.name:
                context = {
                    # 'form': UploadFileForm(),
                    'error_message': 'Entry is forbidden. This vehicle is blocked.'
                }
                return render(request, "plate_recognition/photo_upload.html", context=context)

        except Vehicle.DoesNotExist:
            context = {
                    # 'form': UploadFileForm(),
                    'error_message': 'Entry is forbidden. This vehicle is not registered.',
                }
            return render(request, "plate_recognition/photo_upload.html", context=context)

        user = vehicle.user
        account = Account.objects.get(user=user)
        if account.check_balance_limit():
            context = {
                    # 'form': UploadFileForm(),
                    'error_message': 'Entry is forbidden. User account balance is insufficient.',
                }
            return render(request, "plate_recognition/photo_upload.html", context=context)

        try:
            session = ParkingSession.objects.get(vehicle=vehicle, status=StatusParkingEnum.ACTIVE.name)
            session.status = StatusParkingEnum.FINISHED.name

        except ParkingSession.DoesNotExist:
            available_spots = ParkingSpot.objects.filter(vehicle__isnull=True)
            if not available_spots.exists():
                context = {
                    'form': form,
                    'error_message': 'No available parking spots.'
                }
                return render(request, 'parking_service/main_page.html', context)

            session = ParkingSession(vehicle=vehicle, status=StatusParkingEnum.ACTIVE.name)
            session.vehicle = vehicle
            session.vehicle_plate_number = vehicle.plate_number
            session.save()

        if session.status == StatusParkingEnum.FINISHED.name:
            session.end_at = timezone.now()
            session.save()
            payment = Payment(
                user=user,
                parking_session_pk=session,
                payment_type=TypePaymentEnum.DEBIT.name)
            payment.save()

    # TODO Повернути на головну сторінку: фото на якому буде виділено рамка з номером, номер засобу, дата та час
    # TODO Інформацію про стан паркування: Початок паркування, (Кінець паркування, Тривалість паркування, Вартість)

    context = {
        'filename': filename,
        'manual_plate_number': manual_plate_number,
        'predict_plate_number': predicted_plate_number,
        'num_img': num_img,
        'session': session,
    }

    return render(request, 'parking_service/main_page.html', context)
