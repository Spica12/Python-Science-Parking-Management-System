from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from . import keyboards
from . import text



def setup(router: Router, bot):
    @router.message(Command("start"))
    async def start_handler(msg: types.Message):
        await msg.answer(
            text.greet, reply_markup=keyboards.menu
        )


    @router.message(F.text == "Меню")
    @router.message(F.text == "Вийти в меню")
    @router.message(F.text == "◀️ Повернутись на початок")
    @router.callback_query(F.data == "menu")
    async def menu(clbck: CallbackQuery):
        await clbck.message.answer(text.greet, reply_markup=keyboards.menu)