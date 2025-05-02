import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        username TEXT,
        full_name TEXT,
        is_active INTEGER DEFAULT 0,
        last_seen TEXT
    )''')
    conn.commit()
    conn.close()

def set_agent_status(telegram_id, username, full_name, status):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM agents WHERE telegram_id=?", (telegram_id,))
    if c.fetchone():
        c.execute("UPDATE agents SET is_active=?, username=?, full_name=? WHERE telegram_id=?",
                  (status, username, full_name, telegram_id))
    else:
        c.execute("INSERT INTO agents (telegram_id, username, full_name, is_active, last_seen) VALUES (?, ?, ?, ?, ?)",
                  (telegram_id, username, full_name, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def update_last_seen(telegram_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("UPDATE agents SET last_seen=? WHERE telegram_id=?", (now, telegram_id))
    conn.commit()
    conn.close()

def get_active_agents():
    now = datetime.now()
    threshold = (now - timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT username, full_name FROM agents WHERE is_active=1 AND last_seen >= ?", (threshold,))
    agents = [{"username": row[0], "full_name": row[1]} for row in c.fetchall()]
    conn.close()
    return agents
