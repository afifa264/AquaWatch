import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('aquawatch.db')

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript('''
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS reports (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      category TEXT NOT NULL,
      location TEXT NOT NULL,
      description TEXT NOT NULL,
      priority TEXT NOT NULL DEFAULT 'Medium',
      status TEXT NOT NULL DEFAULT 'Open',
      user_id INTEGER,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
    ''')
    count = db.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
    if count == 0:
        demo = [
          ('Pipe leakage near library', 'Leakage', 'Library Main Road', 'Water is continuously flowing from a damaged joint near the library entrance.', 'Critical', 'Open', None, '2026-10-17 08:40'),
          ('Unusual taste in cafeteria water', 'Water quality', 'Cafeteria Block', 'Students noticed a change in taste and slight discoloration. Please arrange a water test.', 'High', 'In progress', None, '2026-10-16 14:15'),
          ('Low water pressure in Hostel A', 'Low pressure', 'Hostel Block A', 'Water pressure has been low at the upper-floor taps since yesterday evening.', 'Medium', 'Resolved', None, '2026-10-15 09:20'),
          ('Water logging near parking area', 'Water logging', 'East Parking Lot', 'Rainwater is collecting near the parking entrance and making the path slippery.', 'High', 'Open', None, '2026-10-14 17:05'),
        ]
        db.executemany('INSERT INTO reports (title, category, location, description, priority, status, user_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', demo)
    db.commit(); db.close()
