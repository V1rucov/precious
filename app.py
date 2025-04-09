from flask import Flask, render_template, jsonify, send_from_directory, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Замените на собственный секретный ключ
PRODUCTS_DIR = "products"


def load_product_data():
    """Reads all product data from the PRODUCTS_DIR."""
    products = []
    for index, folder_name in enumerate(os.listdir(PRODUCTS_DIR)):
        folder_path = os.path.join(PRODUCTS_DIR, folder_name)
        if os.path.isdir(folder_path):
            product = {
                "id": index,
                "name": folder_name,
                "images": [],
                "description": "",
                "sizes": [],
                "colors": [],
                "price": None,
            }
            for file in os.listdir(folder_path):
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    product["images"].append(f"/products/{folder_name}/{file}")
            desc_file = os.path.join(folder_path, "desc.txt")
            if os.path.exists(desc_file):
                with open(desc_file, "r", encoding="utf-8") as f:
                    product["description"] = f.read().strip()
            size_file = os.path.join(folder_path, "size.txt")
            if os.path.exists(size_file):
                with open(size_file, "r", encoding="utf-8") as f:
                    product["sizes"] = [line.strip() for line in f if line.strip()]
            color_file = os.path.join(folder_path, "color.txt")
            if os.path.exists(color_file):
                with open(color_file, "r", encoding="utf-8") as f:
                    product["colors"] = [line.strip() for line in f if line.strip()]
            price_file = os.path.join(folder_path, "price.txt")
            if os.path.exists(price_file):
                with open(price_file, "r", encoding="utf-8") as f:
                    product["price"] = f.read().strip()
            products.append(product)
    return products


@app.route("/")
def index():
    """Render the homepage."""
    products = load_product_data()
    return render_template("index.html", products=products)


@app.route("/product/<int:product_id>")
def product_page(product_id):
    """Render an individual product page."""
    products = load_product_data()
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template("product.html", product=product)


@app.route("/cart", methods=["POST"])
def add_to_cart():
    """Add a product to the cart."""
    data = request.get_json()
    product_id = data.get("product_id")
    size = data.get("size")
    color = data.get("color")

    # Проверяем, существует ли товар с таким ID
    products = load_product_data()
    for cc in products:
        print(cc["id"])
    product = next((p for p in products if p["id"] == int(product_id)), None)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    # Добавляем товар в корзину
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append({
        "product_id": product_id,
        "size": size,
        "color": color,
    })
    session.modified = True
    return jsonify({"status": "success"})


@app.route("/cart/<int:item_index>", methods=["DELETE"])
def remove_from_cart(item_index):
    """Remove a product from the cart."""
    if "cart" in session and 0 <= item_index < len(session["cart"]):
        session["cart"].pop(item_index)
        session.modified = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Item not found"}), 404


@app.route("/cart")
def get_cart():
    """Get the current cart contents."""
    cart = session.get("cart", [])
    products = load_product_data()

    print("Загруженные продукты:", products)  # Проверяем, загружаются ли товары

    cart_details = []
    for item in cart:
        print("Ищем продукт с ID:", item["product_id"])
        product = next((p for p in products if p["id"] == int(item["product_id"])), None)

        if product is None:
            print(f"⚠ Ошибка: продукт с ID {item['product_id']} не найден!")

        cart_details.append({
            "product": product if product else {"name": "Не найден"},
            "size": item["size"],
            "color": item["color"],
        })

    return jsonify(cart_details)


@app.route("/products/<path:filename>")
def product_file(filename):
    """Serve product images and files."""
    return send_from_directory(PRODUCTS_DIR, filename)

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    if not data or "contacts" not in data or "items" not in data:
        return jsonify({"error": "Некорректные данные"}), 400

    # Отправляем заказ через бота
    asyncio.run(send_order_notification(data))

    return jsonify({"message": "Заказ принят"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(ssl_context=('/etc/letsencrypt/live/shop.preciousforyou.ru/fullchain.pem', '/etc/letsencrypt/live/shop.preciousforyou.ru/privkey.pem'),host='0.0.0.0',port=5000,debug=True)

