"""
Database layer for FAANG Prep App
Uses SQLite via SQLAlchemy for persistence
"""
import sqlite3
import os
import json
import hashlib
import bcrypt
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "faang_prep.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            avatar_color TEXT DEFAULT '#6366f1',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            badges TEXT DEFAULT '[]',
            streak INTEGER DEFAULT 0,
            last_login TEXT,
            is_dev INTEGER DEFAULT 0
        )
    """)

    # Notes table
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Custom links table
    c.execute("""
        CREATE TABLE IF NOT EXISTS custom_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            url TEXT,
            category TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # API tokens table
    c.execute("""
        CREATE TABLE IF NOT EXISTS api_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            github_token TEXT,
            leetcode_username TEXT,
            codeforces_handle TEXT,
            codechef_handle TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Fitness logs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS fitness_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            workout_type TEXT,
            duration_minutes INTEGER,
            calories INTEGER,
            notes TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Progress heatmap table
    c.execute("""
        CREATE TABLE IF NOT EXISTS progress_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            activity_type TEXT,
            count INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Dev uploads table
    c.execute("""
        CREATE TABLE IF NOT EXISTS dev_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filepath TEXT,
            description TEXT,
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # User wallpapers
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            wallpaper_path TEXT,
            theme TEXT DEFAULT 'dark',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# ── User CRUD ──────────────────────────────────────────────
def create_user(username: str, password: str, email: str = "") -> dict:
    conn = get_connection()
    c = conn.cursor()
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    colors = ["#6366f1","#ec4899","#f59e0b","#10b981","#3b82f6","#8b5cf6"]
    import random
    color = random.choice(colors)
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, email, avatar_color) VALUES (?,?,?,?)",
            (username, pw_hash, email, color)
        )
        conn.commit()
        return {"success": True, "message": "Account created!"}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Username already exists."}
    finally:
        conn.close()

def verify_user(username: str, password: str) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
        # update last_login
        conn2 = get_connection()
        conn2.execute("UPDATE users SET last_login=? WHERE id=?", (datetime.now().isoformat(), row["id"]))
        conn2.commit()
        conn2.close()
        return {"success": True, "user": dict(row)}
    return {"success": False, "message": "Invalid username or password."}

def get_user(user_id: int) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {}

def update_streak(user_id: int, streak: int):
    conn = get_connection()
    conn.execute("UPDATE users SET streak=? WHERE id=?", (streak, user_id))
    conn.commit()
    conn.close()

def add_badge(user_id: int, badge: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT badges FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    if row:
        badges = json.loads(row["badges"] or "[]")
        if badge not in badges:
            badges.append(badge)
            conn.execute("UPDATE users SET badges=? WHERE id=?", (json.dumps(badges), user_id))
            conn.commit()
    conn.close()

# ── Notes CRUD ─────────────────────────────────────────────
def save_note(user_id: int, title: str, content: str) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO notes (user_id, title, content) VALUES (?,?,?)",
        (user_id, title, content)
    )
    conn.commit()
    note_id = c.lastrowid
    conn.close()
    return note_id

def update_note(note_id: int, title: str, content: str):
    conn = get_connection()
    conn.execute(
        "UPDATE notes SET title=?, content=?, updated_at=? WHERE id=?",
        (title, content, datetime.now().isoformat(), note_id)
    )
    conn.commit()
    conn.close()

def get_notes(user_id: int) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM notes WHERE user_id=? ORDER BY updated_at DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_note(note_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

# ── Custom Links ───────────────────────────────────────────
def save_link(user_id: int, name: str, url: str, category: str, description: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO custom_links (user_id, name, url, category, description) VALUES (?,?,?,?,?)",
        (user_id, name, url, category, description)
    )
    conn.commit()
    conn.close()

def get_links(user_id: int) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM custom_links WHERE user_id=? ORDER BY category", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_link(link_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM custom_links WHERE id=?", (link_id,))
    conn.commit()
    conn.close()

# ── API Tokens ─────────────────────────────────────────────
def save_api_tokens(user_id: int, github="", leetcode="", codeforces="", codechef=""):
    conn = get_connection()
    conn.execute("""
        INSERT INTO api_tokens (user_id, github_token, leetcode_username, codeforces_handle, codechef_handle)
        VALUES (?,?,?,?,?)
        ON CONFLICT(user_id) DO UPDATE SET
            github_token=excluded.github_token,
            leetcode_username=excluded.leetcode_username,
            codeforces_handle=excluded.codeforces_handle,
            codechef_handle=excluded.codechef_handle
    """, (user_id, github, leetcode, codeforces, codechef))
    conn.commit()
    conn.close()

def get_api_tokens(user_id: int) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM api_tokens WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {}

# ── Fitness ────────────────────────────────────────────────
def log_fitness(user_id: int, date: str, workout_type: str, duration: int, calories: int, notes: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO fitness_logs (user_id, date, workout_type, duration_minutes, calories, notes) VALUES (?,?,?,?,?,?)",
        (user_id, date, workout_type, duration, calories, notes)
    )
    conn.commit()
    conn.close()

def get_fitness_logs(user_id: int) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM fitness_logs WHERE user_id=? ORDER BY date DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

# ── Progress ───────────────────────────────────────────────
def log_progress(user_id: int, date: str, activity_type: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, count FROM progress_logs WHERE user_id=? AND date=? AND activity_type=?",
        (user_id, date, activity_type)
    )
    row = c.fetchone()
    if row:
        conn.execute("UPDATE progress_logs SET count=count+1 WHERE id=?", (row["id"],))
    else:
        conn.execute(
            "INSERT INTO progress_logs (user_id, date, activity_type) VALUES (?,?,?)",
            (user_id, date, activity_type)
        )
    conn.commit()
    conn.close()

def get_progress(user_id: int) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM progress_logs WHERE user_id=?", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

# ── Dev uploads ────────────────────────────────────────────
def save_dev_upload(filename: str, filepath: str, description: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO dev_uploads (filename, filepath, description) VALUES (?,?,?)",
        (filename, filepath, description)
    )
    conn.commit()
    conn.close()

def get_dev_uploads() -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM dev_uploads ORDER BY uploaded_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

# ── User settings ──────────────────────────────────────────
def save_wallpaper(user_id: int, wallpaper_path: str):
    conn = get_connection()
    conn.execute("""
        INSERT INTO user_settings (user_id, wallpaper_path)
        VALUES (?,?)
        ON CONFLICT(user_id) DO UPDATE SET wallpaper_path=excluded.wallpaper_path
    """, (user_id, wallpaper_path))
    conn.commit()
    conn.close()

def get_user_settings(user_id: int) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM user_settings WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {}

init_db()
