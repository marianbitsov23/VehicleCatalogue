import sqlite3

DB_NAME = 'vehicle.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS sales
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        model TEXT,
        horsepower INTEGER,
        price DOUBLE,
        year DATE,
        condition TEXT,
        mileage DOUBLE,
        category_id INTEGER,
        file_path TEXT,
        user_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(id)
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS comments
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        message TEXT,
        user_id INTEGER,
        username TEXT,
        FOREIGN KEY(sale_id) REFERENCES sales(id)
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS categories
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT
    )
''')
conn.commit()

class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()