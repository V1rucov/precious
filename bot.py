import logging
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

TOKEN = "8032192542:AAE-mmWaOBBVtbubkZfLOWICvqmubkaoKxg"
ADMIN_ID = "1496419877"

logging.basicConfig(level=logging.INFO)

async def send_order_notification(order_data, pdata, products):
    try:
        bot = Bot(token=TOKEN)

        text = f"📦 *Новый заказ!*\n\n👤 *Контакты клиента:*\n{order_data['contacts']}\n\n🛍 *Список товаров:*\n"

        for item in pdata:
            pid = int(item.get('product_id'))  # 👈 приводим к int
            product = next((p for p in products if p['id'] == pid), None)

            if product:
                product_name = product['name']
                size = item.get('size', 'Не указан')
                color = item.get('color', 'Не указан')
                text += f" - {product_name} (Размер: {size}, Цвет: {color})\n"
            else:
                text += f" - ❗️Неизвестный товар (ID: {pid})\n"

        await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode=ParseMode.MARKDOWN)
        await bot.session.close()

    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")
