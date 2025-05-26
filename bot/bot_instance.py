# your_telegram_bot_project/bot/bot_instance.py

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.settings import BOT_TOKEN  # Импортируем токен из настроек Django

# Инициализация бота
bot = Bot(token=BOT_TOKEN)


storage = MemoryStorage()

# Инициализация диспетчера
dp = Dispatcher(storage=storage)
