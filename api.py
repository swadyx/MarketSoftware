from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
from dbADIS import add_data, delete_data

app = Flask(__name__)
CORS(app)


def get_connection():
    return psycopg2.connect(
        database="postgres",
        user="postgres",
        password="Eetu2008!",  # ← Change this to your actual password
        host="127.0.0.1",
        port=5432
    )


@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


@app.route('/api/products', methods=['GET'])
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tuotteet;")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return jsonify([dict(zip(col_names, row)) for row in rows])


@app.route('/api/products/check/<name>', methods=['GET'])
def check_product_exists(name):
    """Check if product with this name already exists"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nimi, hinta, maara FROM tuotteet WHERE nimi = %s;", (name.lower(),))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return jsonify({
            "exists": True,
            "product": {"id": row[0], "nimi": row[1], "hinta": float(row[2]), "maara": row[3]}
        })
    return jsonify({"exists": False})


@app.route('/api/products', methods=['POST'])
def add_product():
    """Add new product - lowercase name automatically"""
    data = request.get_json()
    name = data['nimi'].lower()

    conn = get_connection()
    add_data(conn, "tuotteet", ("nimi", "hinta", "maara"),
             (name, data['hinta'], data['maara']))
    conn.close()
    return jsonify({"message": "Product added"}), 201


@app.route('/api/products/<int:id>/add-quantity', methods=['PUT'])
def add_quantity(id):
    """Add quantity to existing product"""
    data = request.get_json()
    amount = data['amount']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tuotteet SET maara = maara + %s WHERE id = %s;", (amount, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Added {amount} to product"})


@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_connection()
    delete_data(conn, "tuotteet", f"id = {id}")
    conn.close()
    return jsonify({"message": "Product deleted"})


@app.route('/api/products/search/name/<name>', methods=['GET'])
def search_product_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tuotteet WHERE nimi ILIKE %s;", (f"%{name}%",))
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return jsonify([dict(zip(col_names, row)) for row in rows])


if __name__ == '__main__':
    app.run(debug=True, port=5000)