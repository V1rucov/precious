import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "TOKEN"
ADMIN_ID = "row_wow"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Логирование
logging.basicConfig(level=logging.INFO)

# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот для уведомлений о заказах.")

# Обработчик заказов
async def send_order_notification(order_data):
    """
    Отправляет заказ в Telegram админу
    """
    try:
        text = f"📦 *Новый заказ!*\n\n👤 *Контакты клиента:* {order_data['contacts']}\n\n🛍 *Список товаров:*\n"
        for item in order_data['items']:
            text += f" - {item['name']} (Размер: {item['size']}, Цвет: {item['color']})\n"

        await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
