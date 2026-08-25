import sqlite3

DB_NAME = "greencycle.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner TEXT NOT NULL,
            phone TEXT NOT NULL,
            district TEXT NOT NULL,
            municipality TEXT NOT NULL,
            address TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waste_collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            waste_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            reward REAL DEFAULT 0,
            collection_date TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compost (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waste_quantity REAL NOT NULL,
            compost_quantity REAL NOT NULL,
            created_date TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_restaurant(name, owner, phone, district, municipality, address):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO restaurants
        (name, owner, phone, district, municipality, address)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, owner, phone, district, municipality, address))

    conn.commit()
    conn.close()


def add_waste(restaurant_id, waste_type, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    # Example reward: ₹5 per kg
    reward = quantity * 5

    cursor.execute("""
        INSERT INTO waste_collections
        (restaurant_id, waste_type, quantity, reward)
        VALUES (?, ?, ?, ?)
    """, (restaurant_id, waste_type, quantity, reward))

    conn.commit()
    conn.close()


def get_restaurants():
    conn = get_connection()

    data = conn.execute("""
        SELECT * FROM restaurants
        ORDER BY id DESC
    """).fetchall()

    conn.close()
    return data


def get_waste_collections():
    conn = get_connection()

    data = conn.execute("""
        SELECT
            waste_collections.id,
            restaurants.name,
            waste_collections.waste_type,
            waste_collections.quantity,
            waste_collections.status,
            waste_collections.reward,
            waste_collections.collection_date
        FROM waste_collections
        JOIN restaurants
        ON waste_collections.restaurant_id = restaurants.id
        ORDER BY waste_collections.id DESC
    """).fetchall()

    conn.close()
    return data


def update_collection(collection_id):
    from datetime import datetime

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE waste_collections
        SET status = 'Collected',
            collection_date = ?
        WHERE id = ?
    """, (datetime.now().strftime("%Y-%m-%d %H:%M"), collection_id))

    conn.commit()
    conn.close()


def add_compost(waste_quantity, compost_quantity):
    from datetime import datetime

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO compost
        (waste_quantity, compost_quantity, created_date)
        VALUES (?, ?, ?)
    """, (
        waste_quantity,
        compost_quantity,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()


def get_compost():
    conn = get_connection()

    data = conn.execute("""
        SELECT * FROM compost
        ORDER BY id DESC
    """).fetchall()

    conn.close()
    return data
