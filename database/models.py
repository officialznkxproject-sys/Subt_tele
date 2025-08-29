import sqlite3
import json
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                 user_id INTEGER UNIQUE, 
                 username TEXT, 
                 is_premium INTEGER DEFAULT 0,
                 premium_until TEXT,
                 created_at TEXT)''')
    
    # Create games table
    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (id INTEGER PRIMARY KEY,
                 user_id INTEGER,
                 game_type TEXT,
                 score INTEGER,
                 played_at TEXT)''')
    
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
                 (user_id, username, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.IntegrityError:
        # User already exists
        pass
    
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'user_id': user[1],
            'username': user[2],
            'is_premium': bool(user[3]),
            'premium_until': user[4],
            'created_at': user[5]
        }
    return None

def update_user_premium(user_id, is_premium):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    premium_until = (datetime.now() + timedelta(days=30)).isoformat() if is_premium else None
    
    c.execute("UPDATE users SET is_premium = ?, premium_until = ? WHERE user_id = ?",
             (int(is_premium), premium_until, user_id))
    
    conn.commit()
    conn.close()

def add_game_score(user_id, game_type, score):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO games (user_id, game_type, score, played_at) VALUES (?, ?, ?, ?)",
             (user_id, game_type, score, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_leaderboard(game_type=None, limit=10):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    if game_type:
        c.execute('''SELECT users.username, games.score 
                    FROM games 
                    JOIN users ON games.user_id = users.user_id 
                    WHERE games.game_type = ? 
                    ORDER BY games.score DESC 
                    LIMIT ?''', (game_type, limit))
    else:
        c.execute('''SELECT users.username, SUM(games.score) as total_score 
                    FROM games 
                    JOIN users ON games.user_id = users.user_id 
                    GROUP BY games.user_id 
                    ORDER BY total_score DESC 
                    LIMIT ?''', (limit,))
    
    leaderboard = c.fetchall()
    conn.close()
    
    return leaderboard
