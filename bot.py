from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import logging
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот для уведомлений о заказах.")

async def send_order_notification(order_data, products):
    try:
        text = f"📦 *Новый заказ!*\n\n👤 *Контакты клиента:* {order_data['contacts']}\n\n🛍 *Список товаров:*\n"
        for item in order_data["items"]:
            pid = int(item.get("product_id"))
            product = next((p for p in products if p["id"] == pid), None)
            name = product["name"] if product else "Неизвестный товар"
            size = item.get("size", "Не указан")
            color = item.get("color", "Не указан")
            text += f" - {name} (Размер: {size}, Цвет: {color})\n"

        await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")

async def main():
    await dp.start_polling(bot)
