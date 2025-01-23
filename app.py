from flask import Flask, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

# Path to the products directory
PRODUCTS_DIR = "products"


def load_product_data():
    """Reads all product data from the PRODUCTS_DIR."""
    products = []
    for folder_name in os.listdir(PRODUCTS_DIR):
        folder_path = os.path.join(PRODUCTS_DIR, folder_name)
        if os.path.isdir(folder_path):
            product = {
                "name": folder_name,
                "images": [],
                "description": "",
                "sizes": [],
                "colors": [],
                "price": None,
            }
            
            # Read images
            for file in os.listdir(folder_path):
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    product["images"].append(f"/products/{folder_name}/{file}")
            
            # Read description
            desc_file = os.path.join(folder_path, "desc.txt")
            if os.path.exists(desc_file):
                with open(desc_file, "r", encoding="utf-8") as f:
                    product["description"] = f.read().strip()
            
            # Read sizes
            size_file = os.path.join(folder_path, "size.txt")
            if os.path.exists(size_file):
                with open(size_file, "r", encoding="utf-8") as f:
                    product["sizes"] = [line.strip() for line in f if line.strip()]
            
            # Read colors
            color_file = os.path.join(folder_path, "color.txt")
            if os.path.exists(color_file):
                with open(color_file, "r", encoding="utf-8") as f:
                    product["colors"] = [line.strip() for line in f if line.strip()]
            
            # Read price
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


@app.route("/products/<path:filename>")
def product_file(filename):
    """Serve product images and files."""
    return send_from_directory(PRODUCTS_DIR, filename)


@app.route("/api/products")
def api_products():
    """API endpoint for fetching product data."""
    products = load_product_data()
    return jsonify(products)


if __name__ == "__main__":
    app.run(debug=True)
