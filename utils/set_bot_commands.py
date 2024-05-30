from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot


async def set_default_commands():
    commands = [
        BotCommand(
            command="start",
            description="Запустить бота."
        ),
        BotCommand(
            command="help",
            description="Помощь."
        ),
        BotCommand(
            command="create_exel",
            description="Создайте файл данных учащихся."
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
