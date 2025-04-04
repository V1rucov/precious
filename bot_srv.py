from flask import Flask, request, jsonify
import asyncio
from bot import send_order_notification

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    if not data or "contacts" not in data or "items" not in data:
        return jsonify({"error": "Некорректные данные"}), 400

    # Отправляем заказ через бота
    asyncio.run(send_order_notification(data))

    return jsonify({"message": "Заказ принят"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
