import os
import re
import csv
import tempfile
import aiofiles

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile

from users.models import CustomUser
from parking_service.models import Vehicle, ParkingSession
from finance.models import Payment
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
            await sync_to_async(user.save)()
            await message.answer(text.greet, reply_markup=keyboards.menu)
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
                all_records = [f'Статус парковки: {record.status}\nТривалість паркування: {record.parking_duration}\nПочаток: {record.started_at}\nЗакінчення: {record.end_at}' for record in records]
                all_records_text = "\n\n".join(all_records)
                await clbck.message.answer(all_records_text, reply_markup=keyboards.exit_kb)
            else:
                await clbck.message.answer(text.dont_have_sessions, reply_markup=keyboards.exit_kb)
        except Vehicle.DoesNotExist:
            await clbck.message.answer(text.dont_have_car, reply_markup=keyboards.exit_kb)
            
    
    @router.callback_query(F.data == "parking_messages")
    async def input_parking_messages(clbck: CallbackQuery):
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=clbck.from_user.id)
        
        vehicles = await sync_to_async(list)(Vehicle.objects.filter(user=user))
        inline_keyboard = []
        if vehicles:
            for vehicle in vehicles:
                button = [InlineKeyboardButton(text=vehicle.plate_number, callback_data=f'messages_{vehicle.id}')]
                inline_keyboard.append(button)
            inline_keyboard.append([InlineKeyboardButton(text="◀️ Повернутись назад", callback_data="menu")])
            vehicle_list = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await clbck.message.answer(text.license_plate, reply_markup=vehicle_list)
        else:
            await clbck.message.answer(text.dont_have_car, reply_markup=keyboards.exit_kb)
        
    @router.callback_query(lambda car: car.data and car.data.startswith('messages_'))
    async def process_callback_parking_messages(clbck: CallbackQuery):
        vehicle_id = int(clbck.data.split('_')[1])
        vehicle = await sync_to_async(Vehicle.objects.get)(id=vehicle_id)
        # records = await sync_to_async(list)(ParkingSession.objects.filter(vehicle_id=vehicle.id))
        # all_sessions_data = []
        # for record in records:
        #     payment = await sync_to_async(Payment.objects.get(parking_session_pk_id=record.id))
        #     all_sessions_data.append(payment)
        
        await clbck.message.answer(text.ok_message, reply_markup=keyboards.exit_kb)
        
    @router.callback_query(F.data == "report")
    async def input_parking_report(clbck: CallbackQuery):
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=clbck.from_user.id)
        vehicle = await sync_to_async(Vehicle.objects.get)(user_id=user.id)
        records = await sync_to_async(list)(ParkingSession.objects.filter(vehicle_id=vehicle.id))
        
        all_sessions_data = []
        for record in records:
            payments = await sync_to_async(list)(Payment.objects.filter(parking_session_pk_id=record.id))
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
            
        await bot.send_document(clbck.from_user.id, FSInputFile(tmp_file_path, filename='parking_sessions.csv'))
        os.remove(tmp_file_path)
        await clbck.message.answer(text.csv_input, reply_markup=keyboards.exit_kb)
    
    
    
    
    # @router.callback_query(F.data == "registration_vehicle")
    # async def input_registration_vehicle(clbck: CallbackQuery):
    #     await clbck.message.answer(text.registration_vehicle, reply_markup=keyboards.exit_kb)
    
    # @router.message(lambda message: re.match(pattern, message.text.upper()))
    # async def handle_license_plate(message: types.Message):
    #     license_plate = message.text.strip().upper()
    #     vehicle = await sync_to_async(Vehicle.objects.get)(plate_number=license_plate)
    #     user = await sync_to_async(CustomUser.objects.get)(id=vehicle.user_id)
    #     user.telegram_id = message.from_user.id
    #     await sync_to_async(user.save)()
    #     await message.answer(f'{user.email}, {text.ok_message}', reply_markup=keyboards.exit_kb)