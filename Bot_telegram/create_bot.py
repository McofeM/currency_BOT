from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from Bot_telegram.handlers.password import token

TOKEN_API = token

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
