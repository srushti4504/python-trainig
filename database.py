import os
import sqlite3
from flask import Flask, render_template, request, flash

# Absolute path to the database in this package's folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "college.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no INTEGER NOT NULL,
            attendance INTEGER DEFAULT 0,
            branch TEXT NOT NULL,
            marks INTEGER NOT NULL,
            year TEXT DEFAULT '1st Year'
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student'
        )
    ''')
    

    try:
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
    except sqlite3.OperationalError:
        pass


    try:
       conn.execute("ALTER TABLE students ADD COLUMN year TEXT DEFAULT '1st Year'")
    except sqlite3.OperationalError:
        pass

    try:
       conn.execute("ALTER TABLE students ADD COLUMN photo TEXT DEFAULT 'default.png'")
    except sqlite3.OperationalError:
        pass


    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()