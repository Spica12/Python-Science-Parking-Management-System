import csv
import tempfile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from adminapp.decorators import admin_or_operator_required
from finance.models import Payment
from users.models import UserRole
from vehicles.models import Vehicle
from vehicles.forms import VehicleForm
from parking_service.models import ParkingSession, StatusParkingEnum
from vehicles.utils import get_total_parking_duration
from users.decorators import user_is_verified

# @user_is_verified (Replace login_required)
@user_is_verified
def get_vehicles(request):
    
    # TODO Зробити більш правильну перевірку на адміна або оператора
    user_role = get_object_or_404(UserRole, user=request.user)
    if user_role.is_admin or user_role.role == 'Operator':
        vehicles = Vehicle.objects.all()
    else:
        vehicles = Vehicle.objects.filter(user=request.user)

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

@login_required(login_url="login")
def generate_report(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    records = ParkingSession.objects.filter(vehicle=vehicle)
    
    all_sessions_data = []
    for record in records:
        payments = Payment.objects.filter(parking_session_pk_id=record.id)
        session_data = {
            'status': record.status,
            'parking_duration': record.parking_duration,
            'started_at': record.started_at,
            'end_at': record.end_at,
            'payments': [(payment.amount, payment.created_at) for payment in payments]
        }
        all_sessions_data.append(session_data)
    
    tmp_file_path = ''
    with tempfile.NamedTemporaryFile(mode='w', newline='', encoding='utf-8', delete=False, suffix='.csv') as tmp_file:
        csv_writer = csv.writer(tmp_file)
        csv_writer.writerow(['Статус', 'Тривалість', 'Початок', 'Закінчення', 'Сума', 'Дата оплати'])
        
        for session in all_sessions_data:
            for payment in session['payments']:
                csv_writer.writerow([
                    session['status'],
                    session['parking_duration'],
                    session['started_at'],
                    session['end_at'],
                    payment[0],
                    payment[1]
                ])
        
        tmp_file_path = tmp_file.name

    response = HttpResponse(open(tmp_file_path, 'rb').read(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="vehicle_{vehicle.plate_number}_report.csv"'
    return response
