from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from dbADIS import add_data, delete_data, search_by_id, search_by_name

app = Flask(__name__)
CORS(app)


# Database connection - update with your credentials
def get_connection():
    return psycopg2.connect(
        database="postgres",
        user="postgres",
        password="your_password",  # Set this via environment variable in production
        host="127.0.0.1",
        port=5432
    )


@app.route('/api/products', methods=['GET'])
def get_all_products():
    """Uses inspect_data logic to get all products"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tuotteet;")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    products = [dict(zip(col_names, row)) for row in rows]
    return jsonify(products)


@app.route('/api/products', methods=['POST'])
def add_product():
    """Uses your add_data function"""
    data = request.get_json()
    conn = get_connection()
    add_data(conn, "tuotteet", ("nimi", "hinta", "maara"),
             (data['nimi'], data['hinta'], data['maara']))
    conn.close()
    return jsonify({"message": "Product added"}), 201


@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """Uses your delete_data function"""
    conn = get_connection()
    delete_data(conn, "tuotteet", f"id = {id}")
    conn.close()
    return jsonify({"message": "Product deleted"})


@app.route('/api/products/search/id/<int:id>', methods=['GET'])
def search_product_by_id(id):
    """Uses your search_by_id function"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tuotteet WHERE id = %s;", (id,))
    row = cursor.fetchone()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    if row:
        return jsonify(dict(zip(col_names, row)))
    return jsonify({"error": "Not found"}), 404


@app.route('/api/products/search/name/<name>', methods=['GET'])
def search_product_by_name(name):
    """Uses your search_by_name logic"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tuotteet WHERE nimi ILIKE %s;", (f"%{name}%",))
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    products = [dict(zip(col_names, row)) for row in rows]
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
