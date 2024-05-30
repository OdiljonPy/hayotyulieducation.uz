import requests
from aiogram import types, Router
from filters.filters import IsAdmin
from data.config import ADMINS, BACKEND_URL
from aiogram.filters import Command, CommandStart

router = Router()


@router.message(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        text="Xush kelibsiz!"
    )


@router.message(Command('create_exel'), IsAdmin(ADMINS))
async def bot_help(message: types.Message):
    result = requests.get(
        url=f"{BACKEND_URL}/authentication/api/students/sheet/{message.from_user.id}/"
    )
    if result.status_code != 200:
        await message.answer(
            text="So'rov yuborishda xatolik bor."
        )
        return


@router.message(Command('create_exel'))
async def bot_help(message: types.Message):
    await message.answer(text="Siz ushbu buyruqdan foydalana olmaysiz")
