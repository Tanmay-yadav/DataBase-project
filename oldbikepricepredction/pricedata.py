import sqlite3

def get_db_connection():
    conn = sqlite3.connect('bike_price.db')  # Connect to the SQLite database
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kms_driven INTEGER,
            owner INTEGER,
            age INTEGER,
            power INTEGER,
            brand TEXT,
            prediction REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_prediction(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (kms_driven, owner, age, power, brand, prediction)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['kms_driven'], data['owner'], data['age'], data['power'], data['brand'], data['prediction']))
    conn.commit()
    conn.close()
