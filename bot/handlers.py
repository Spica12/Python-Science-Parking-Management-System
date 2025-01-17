import asyncio
import os
import re
import csv
import tempfile

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile

from users.models import CustomUser
from parking_service.models import StatusParkingEnum, Vehicle, ParkingSession
from finance.models import Account, Payment
from . import keyboards
from . import text

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def setup(router: Router, bot):
    @router.message(Command("start"))
    async def start_handler(message: types.Message):
        await message.answer(text.enter_email)
        
    @router.message(lambda message: re.match(email_regex, message.text))
    async def handle_license_plate(message: types.Message):
        email = message.text.strip()
        try:
            user = await sync_to_async(CustomUser.objects.get)(email=email)
            user.telegram_id = message.from_user.id
            user.is_tg_verified = False
            await sync_to_async(user.save)()
            await message.answer(text.verify)
            while True:
                user = await sync_to_async(CustomUser.objects.get)(email=email)
                if user.is_tg_verified:
                    await message.answer(text.greet, reply_markup=keyboards.menu)
                    break
                await asyncio.sleep(5)
        except CustomUser.DoesNotExist:
            await message.answer(text.error_message_1)

    @router.callback_query(F.data == "menu")
    async def menu(clbck: CallbackQuery):
        await clbck.message.answer(text.greet, reply_markup=keyboards.menu)
        
    @router.callback_query(F.data == "vehicles")
    async def input_vehicles(clbck: CallbackQuery):
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=clbck.from_user.id)
        
        vehicles = await sync_to_async(list)(Vehicle.objects.filter(user=user))
        inline_keyboard = []
        if vehicles:
            for vehicle in vehicles:
                button = [InlineKeyboardButton(text=vehicle.plate_number, callback_data=f'vehicles_{vehicle.id}')]
                inline_keyboard.append(button)
            inline_keyboard.append([InlineKeyboardButton(text="◀️ Повернутись назад", callback_data="menu")])
            vehicle_list = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await clbck.message.answer(text.choose_car, reply_markup=vehicle_list)
        else:
            await clbck.message.answer(text.dont_have_car, reply_markup=keyboards.exit_kb)
            
    @router.callback_query(lambda car: car.data and car.data.startswith('vehicles_'))
    async def process_callback_vehicle(clbck: CallbackQuery):
        vehicle_id = int(clbck.data.split('_')[1])
        try:
            vehicle = await sync_to_async(Vehicle.objects.get)(id=vehicle_id)
            records = await sync_to_async(list)(ParkingSession.objects.filter(vehicle_id=vehicle.id))
            if records:
                records = sorted(records, key=lambda x: x.started_at)
                all_sessions_data = []
                for record in records:
                    try:
                        payment = await sync_to_async(Payment.objects.get)(parking_session_pk_id=record.id)
                        session_data = {
                            'status': record.status,
                            'parking_duration': record.parking_duration,
                            'started_at': record.started_at,
                            'end_at': record.end_at,
                            'payment': payment.amount
                        }
                    except Payment.DoesNotExist:
                        session_data = {
                            'status': record.status,
                            'parking_duration': record.parking_duration,
                            'started_at': record.started_at,
                            'end_at': record.end_at,
                            'payment': 'No payment'
                        }
                    all_sessions_data.append(session_data)
                        
                all_records = [f"Статус парковки: {session['status']}\nТривалість паркування: {session['parking_duration']}\nПочаток: {session['started_at']}\nЗакінчення: {session['end_at']}\nЦіна: {session['payment']}" for session in all_sessions_data]
                all_records_text = "\n\n".join(all_records)
                await clbck.message.answer(all_records_text, reply_markup=keyboards.exit_kb)
            else:
                await clbck.message.answer(text.dont_have_sessions, reply_markup=keyboards.exit_kb)
        except Vehicle.DoesNotExist:
            await clbck.message.answer(text.dont_have_car, reply_markup=keyboards.exit_kb)
            
    async def monitor_balance(clbck: CallbackQuery, user):
        notified = False
        while True:
            balance = await sync_to_async(Account.objects.get)(user=user)
            if balance.check_balance_limit():
                if not notified:
                    await clbck.message.answer(text.limits_alert)
                    notified = True
            else:
                notified = False
            await asyncio.sleep(5)
    
    @router.callback_query(F.data == "parking_messages")
    async def input_parking_messages(clbck: CallbackQuery):
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=clbck.from_user.id)
        await clbck.message.answer(text.ok_message, reply_markup=keyboards.exit_kb)
        asyncio.create_task(monitor_balance(clbck, user))
        
    @router.callback_query(F.data == "report")
    async def input_report(clbck: CallbackQuery):
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=clbck.from_user.id)
        
        vehicles = await sync_to_async(list)(Vehicle.objects.filter(user=user))
        inline_keyboard = []
        if vehicles:
            for vehicle in vehicles:
                button = [InlineKeyboardButton(text=vehicle.plate_number, callback_data=f'reports_{vehicle.id}')]
                inline_keyboard.append(button)
            inline_keyboard.append([InlineKeyboardButton(text="◀️ Повернутись назад", callback_data="menu")])
            vehicle_list = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await clbck.message.answer(text.report, reply_markup=vehicle_list)
        else:
            await clbck.message.answer(text.dont_have_car, reply_markup=keyboards.exit_kb)
        
    @router.callback_query(lambda car: car.data and car.data.startswith('reports_'))
    async def process_callback_report(clbck: CallbackQuery):
        vehicle_id = int(clbck.data.split('_')[1])
        vehicle = await sync_to_async(Vehicle.objects.get)(id=vehicle_id)
        records = await sync_to_async(list)(ParkingSession.objects.filter(vehicle_id=vehicle.id, status=StatusParkingEnum.FINISHED.name))
        if records:
            records = sorted(records, key=lambda x: x.started_at)
            all_sessions_data = []
            for record in records:
                try:
                    payment = await sync_to_async(Payment.objects.get)(parking_session_pk_id=record.id)
                    session_data = {
                        'id': record.id,
                        'status': record.status,
                        'parking_duration': record.parking_duration,
                        'started_at': record.started_at,
                        'end_at': record.end_at,
                        'payments': [payment.amount, payment.created_at]
                    }
                except Payment.DoesNotExist:
                    session_data = {
                        'status': record.status,
                        'parking_duration': record.parking_duration,
                        'started_at': record.started_at,
                        'end_at': record.end_at,
                        'payment': ['No payment', 'No payment']
                    }
                all_sessions_data.append(session_data)
            
            tmp_file_path = ''
            with tempfile.NamedTemporaryFile(mode='w', newline='', encoding='utf-8', delete=False, suffix='.csv') as tmp_file:
                csv_writer = csv.writer(tmp_file)
                csv_writer.writerow(['Parking Session', 'Status', 'Parking duration', 'Started at', 'End at', 'Amount', 'Payment date'])
                
                for session in all_sessions_data:
                    csv_writer.writerow([
                        session['id'],
                        session['status'],
                        session['parking_duration'],
                        session['started_at'],
                        session['end_at'],
                        session['payments'][0],
                        session['payments'][1]
                    ])
                
                tmp_file_path = tmp_file.name
                
            await bot.send_document(clbck.from_user.id, FSInputFile(tmp_file_path, filename='parking_sessions.csv'))
            os.remove(tmp_file_path)
            await clbck.message.answer(text.csv_input, reply_markup=keyboards.exit_kb)
        else:
            await clbck.message.answer(text.dont_have_sessions, reply_markup=keyboards.exit_kb)