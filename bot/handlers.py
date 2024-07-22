import re

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery

from . import keyboards
from . import text

pattern = r'^[A-Z]{2}\d{4}[A-Z]{2}$'

def setup(router: Router, bot):
    @router.message(Command("start"))
    async def start_handler(message: types.Message):
        await message.answer(
            text.greet, reply_markup=keyboards.menu
        )


    @router.message(F.text == "Меню")
    @router.message(F.text == "Вийти в меню")
    @router.message(F.text == "◀️ Повернутись на початок")
    @router.callback_query(F.data == "menu")
    async def menu(clbck: CallbackQuery):
        await clbck.message.answer(text.greet, reply_markup=keyboards.menu)
        
    @router.callback_query(F.data == "parking_messages")
    async def input_parking_messages(clbck: CallbackQuery):
        await clbck.message.answer(text.license_plate, reply_markup=keyboards.exit_kb)
        
    @router.message(lambda message: re.match(pattern, message.text.upper()))
    async def handle_license_plate(message: types.Message):
        license_plate = message.text.strip().upper()
        try:
            await message.answer(text.ok_message, reply_markup=keyboards.exit_kb)
        except Exception as e:
            await message.answer(text.error_message, reply_markup=keyboards.exit_kb)