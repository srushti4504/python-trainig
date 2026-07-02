import sqlite3
from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = "college123" 

# 2 functions
def get_db():
   
   conn = sqlite3.connect("database.db")
   conn.row_factory = sqlite3.Row
   return conn

def init_db():
    
    """Create table"""""
    conn = get_db()
    # Create students table if it doesn't exist
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll_no INTEGER NOT NULL,
                 Attendance INTEGER DEFAULT 0 ,
                    branch TEXT NOT NULL,
                    Marks TEXT NOT NULL
                 )
                    ''')
            
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS users (
                 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                 role Text Defaulit 'student'
                 )
                    ''')

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "College Smart Portal Running Successfully"

def get_db():
    conn = sqlite3.connect("college.db")
    return conn

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)
