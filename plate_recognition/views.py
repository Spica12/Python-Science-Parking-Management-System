from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from finance.models import Account, Payment
from parking_service.models import ParkingSession, StatusParkingEnum
from vehicles.models import Vehicle, StatusVehicleEnum
from plate_recognition.forms import UploadFileForm, ConfirmPlateForm
from plate_recognition.service_predict import image_plate_recognition
from parking_service.models import ParkingSpot

import logging
logging.basicConfig(level=logging.INFO)

# Create your views here.
def upload_photo(request):
    logging.debug('Start upload photo')

    filename = ''
    manual_plate_number = ''
    plate_number = ''


    request.session['predicted_plate_number'] = ''
    request.session['confirmed_plate_number'] = ''
    request.session['num_img'] = ''
    request.session['filename'] = ''

    if request.method == "POST":
        logging.debug('if method POST')
        # Приймання зображень від користувача
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logging.debug('If form is valid')
            # uploaded_image = request.FILES.get("image")
            # manual_plate_number = request.POST.get("manual_plate_number")
            uploaded_image = form.cleaned_data.get('image')
            manual_plate_number = form.cleaned_data.get('manual_plate_number')

            logging.debug(f'manual_plate_number {manual_plate_number}')

            # TODO Зробити логіку вибору між ручним номером та номером з фото. Поки що вибір ручного вводу номера
            if not uploaded_image and not manual_plate_number:
                logging.debug('not image and not manual plate')
                context = {
                    'form': form,
                    'error_message': 'You need enter manual plate number or upload image.'
                }
                return render(request, "plate_recognition/photo_upload.html", context)
            if uploaded_image and not manual_plate_number:
                logging.debug('image and not manual plate')
                # Детекція номерного знаку
                # Виявлення та виділення області з номерним знаком із зображень.
                # Оптичне розпізнавання символів для ідентифікації тексту номерного знаку.
                img_predict = image_plate_recognition.predict_plate(file=uploaded_image)

                request.session['predicted_plate_number'] = img_predict.get('num_vehicle_str')
                request.session['num_img'] = img_predict.get('num_img')
                request.session['filename'] = uploaded_image.name

                # return redirect('plate_recognition:confirm_plate_number')
            if manual_plate_number:
                logging.debug('entered manual plate')
                request.session['confirmed_plate_number'] = manual_plate_number

            logging.debug('return redirect to confirm_plate_number')
            return redirect('plate_recognition:confirm_plate_number')

    else:
        logging.debug('if method GET')
        form = UploadFileForm()

    logging.debug('render photo_upload')
    return render(
        request,
        "plate_recognition/photo_upload.html",
        {"form": form}
    )


def confirm_plate_number(request):
    logging.debug('Start confirm_plate_number')
    predicted_plate_number = request.session.get('predicted_plate_number', '')
    confirmed_plate_number = request.session.get('confirmed_plate_number', '')
    manual_plate_number = request.session.get('confirmed_plate_number', '')
    num_img = request.session.get('num_img', '')
    filename = request.session.get('filename', '')
    logging.debug(f'predicted_plate_number: {predicted_plate_number}')
    logging.debug(f'confirmed_plate_number: {confirmed_plate_number}')
    logging.debug(f'manual_plate_number: {manual_plate_number}')
    logging.debug(f'filename: {filename}')

    if request.method == 'POST' and not confirmed_plate_number:
        logging.debug('if method POST and not confirmed number')
        form = ConfirmPlateForm(request.POST)
        if form.is_valid():
            logging.debug('if form is valid')
            confirmed_plate_number = form.cleaned_data.get('confirm_plate_number')
            logging.debug(f'confirmed_plate_number: {confirmed_plate_number}')
            request.session.pop('filename', None)
            # request.session.pop('confirmed_plate_number', None)
            # request.session.pop('predicted_plate_number', None)
            request.session.pop('num_img', None)

    elif request.method == 'GET' and not confirmed_plate_number:
        logging.debug('if method GET and not confirmed number')
        form = ConfirmPlateForm(initial={'confirm_plate_number': predicted_plate_number})

        context = {
            'form': form,
            'predict_plate_number': predicted_plate_number,
            'num_img': num_img,
        }
        logging.debug('render confirm_plate_number.html')
        return render(request, 'plate_recognition/confirm_plate_number.html', context=context)

    if confirmed_plate_number:
        logging.debug('if confirm_plate_number')
        # TODO Пошук номера авто у базі даних зареєстрованих транспортних засобів.
        # TODO Додати перевірку Якщо машина заблокована, то вивести інформацію, що засіб заблокований

        form = None

        try:
            vehicle = Vehicle.objects.get(plate_number=confirmed_plate_number)
            if vehicle.status == StatusVehicleEnum.BLOCKED.name:
                logging.debug('vehicle is blocked')
                context = {
                    # 'form': UploadFileForm(),
                    'error_message': 'Entry is forbidden. This vehicle is blocked.'
                }
                return render(request, "plate_recognition/photo_upload.html", context=context)

        except Vehicle.DoesNotExist:
            logging.debug('vehicle does not exist')
            context = {
                    # 'form': UploadFileForm(),
                    'error_message': 'Entry is forbidden. This vehicle is not registered.',
                }
            return render(request, "plate_recognition/photo_upload.html", context=context)

        user = vehicle.user
        account = Account.objects.get(user=user)
        if account.check_balance_limit():
            logging.debug('User account balance is insufficient')
            context = {
                    # 'form': UploadFileForm(),
                    'error_message': 'Entry is forbidden. User account balance is insufficient.',
                }
            return render(request, "plate_recognition/photo_upload.html", context=context)

        try:
            session = ParkingSession.objects.get(vehicle=vehicle, status=StatusParkingEnum.ACTIVE.name)
            session.status = StatusParkingEnum.FINISHED.name
            logging.debug('try session is finished')

        except ParkingSession.DoesNotExist:
            available_spots = ParkingSpot.objects.filter(vehicle__isnull=True)
            if not available_spots.exists():
                logging.debug('No available parking spots')
                context = {
                    'form': form,
                    'error_message': 'No available parking spots.'
                }
                return render(request, 'parking_service/main_page.html', context)

            session = ParkingSession(vehicle=vehicle, status=StatusParkingEnum.ACTIVE.name)
            session.vehicle = vehicle
            session.vehicle_plate_number = vehicle.plate_number
            session.save()
            logging.debug('create session')

        if session.status == StatusParkingEnum.FINISHED.name:
            logging.debug('session is finished and create Payment')
            session.end_at = timezone.now()
            session.save()
            payment = Payment(parking_session_pk=session)
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
    logging.debug('End confirm_plate_number and render parking_service/main_page.html')
    return render(request, 'plate_recognition/photo_upload_result.html', context)
