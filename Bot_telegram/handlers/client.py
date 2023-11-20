import aioschedule as schedule
import asyncio
from aiogram import types, Dispatcher
from Bot_telegram.create_bot import bot
from datetime import datetime
import pymongo
from Bot_telegram.handlers.password import mangodbpassword
from Bot_telegram.handlers.other import course


mongo_client = pymongo.MongoClient(f"mongodb+srv://{mangodbpassword}@cluster0.inrqtd0.mongodb.net/")
db = mongo_client.Telegram_bot
collection = db["Telegram_bot"]

data_storage = []


async def add_user(user_id):
    date = datetime.now().date()
    print(f"Додавання користувача {user_id} з датою {date} до бази даних.")
    result = collection.insert_one({
        "_id": user_id,
        "date": str(date)
    })

    if result.acknowledged:
        print(f"Дані користувача {user_id} були успішно додані.")
    else:
        print(f"Помилка під час додавання даних користувачу {user_id}.")


async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Дізнатися ситуацію на ринку")
    markup.add(btn1)
    await bot.send_message(message.from_user.id, f"Привіт {message.from_user.first_name}! Я бот який допоможе тобі з кріптоволютою ", reply_markup=markup)
    await add_user(message.chat.id)


async def handle_text(message: types.Message):
    if message.text == "Дізнатися ситуацію на ринку":
        for i in range(0, len(data_storage), 2):
            markup = types.InlineKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("Подивитись детальнеше", url=data_storage[i])
            markup.add(btn)
            await bot.send_message(message.from_user.id, data_storage[i+1], reply_markup=markup)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(handle_text, content_types=['text'])


async def scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

data = course("https://whitebit.com/ua/markets")
if data:
    if isinstance(data[0], str) and "Помилка" in data[0]:
        print(data[0])
    else:
        data_storage.clear()
        data_storage.extend(data)
        print("бот зібрав дані")
