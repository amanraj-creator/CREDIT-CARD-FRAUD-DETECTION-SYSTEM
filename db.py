import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_number TEXT,
        time TEXT,
        amount REAL,
        merchant TEXT
    )
""")
conn.commit()
conn.close()
