import psycopg2


def add_data(conn, table_name, columns, values):
    try:
        cursor = conn.cursor()
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
        cursor.execute(query, values)
        conn.commit()
        print(f"Data added to '{table_name}' successfully!")
        cursor.close()
    except Exception as e:
        print(f"Error adding data: {e}")
        conn.rollback()


def delete_data(conn, table_name, condition):
    try:
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name} WHERE {condition};"
        cursor.execute(query)
        conn.commit()
        print(f"Deleted {cursor.rowcount} row(s) from '{table_name}'.")
        cursor.close()
    except Exception as e:
        print(f"Error deleting data: {e}")
        conn.rollback()


def inspect_data(conn, table_name, limit=None):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        query += ";"

        cursor.execute(query)
        rows = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]

        print(f"\n--- Table: {table_name} ({len(rows)} rows) ---")
        print(" | ".join(col_names))
        print("-" * 50)

        for row in rows:
            print(" | ".join(str(val) for val in row))

        print()
        cursor.close()
    except Exception as e:
        print(f"Error inspecting data: {e}")


def search_by_id(conn, table_name, id_value):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE id = %s;"
        cursor.execute(query, (id_value,))
        row = cursor.fetchone()

        if row:
            col_names = [desc[0] for desc in cursor.description]
            print(f"\n--- Found record with ID: {id_value} ---")
            print(" | ".join(col_names))
            print("-" * 50)
            print(" | ".join(str(val) for val in row))
            print()
        else:
            print(f"No record found with ID: {id_value}")

        cursor.close()
        return row
    except Exception as e:
        print(f"Error searching by ID: {e}")
        return None


def search_by_name(conn, table_name, name_value, name_column="name"):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {name_column} ILIKE %s;"
        cursor.execute(query, (f"%{name_value}%",))
        rows = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]

        print(f"\n--- Search by name: '{name_value}' ---")
        print(f"Found {len(rows)} result(s)")
        print(" | ".join(col_names))
        print("-" * 50)

        for row in rows:
            print(" | ".join(str(val) for val in row))

        print()
        cursor.close()
        return rows
    except Exception as e:
        print(f"Error searching by name: {e}")
        return []