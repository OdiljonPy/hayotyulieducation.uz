from aiogram import Router
from . import start
from . import help
from . import echo

user_router = Router()
user_router.include_routers(
    start.router,
    help.router,
    echo.router,
)

