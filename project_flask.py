from http import client

from click import prompt
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, flash,session
from database import BASE_DIR, get_db ,init_db
from groq import Groq
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename

load_dotenv()  # Load environment variables from .env file


# Configure Flask with explicit static folder path
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
app.secret_key = "college 123"


UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the upload folder if it doesn't exist

def allowed_file(filename):
    #only allow certain file extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




students = [
    {"id": 1, "name": "Aarav", "branch": "Computer", "attendance": "92%", "marks": 85},
    {"id": 2, "name": "Priya", "branch": "Mechanical", "attendance": "88%", "marks": 78},
    {"id": 3, "name": "Rahul", "branch": "Electrical", "attendance": "95%", "marks": 90},
    {"id": 4, "name": "Sneha", "branch": "Civil", "attendance": "89%", "marks": 82},
    {"id": 5, "name": "Rohan", "branch": "Computer", "attendance": "97%", "marks": 91}
]

notice_items = [
    "Python Internship started on 28 May.",
    "Sir announced that,",
    "To encourage learning, consistency, and active participation,",
    "a special competition has been announced.",
    "At the end of the training,",
    "The Top 5 performing students will be selected and rewarded with a special gift."
]



@app.route("/")
def home():

    conn = get_db()

    students = conn.execute("SELECT * FROM students" ).fetchall()

    return render_template("home.html", students=students, notices=notice_items)

@app.route("/notices")
def notices():
    return render_template("notices.html", notices=notice_items)

@app.route("/search")
def search():
    q = request.args.get("q", "")

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    students = cursor.execute("""
        SELECT id, name, roll_no, branch, attendance, marks
        FROM students
        WHERE name LIKE ?
        OR CAST(roll_no AS TEXT) LIKE ?
        OR branch LIKE ?
    """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()

    conn.close()

    return render_template(
        "search.html",
        students=students
    )

@app.route("/filter")
def filter():

    selected_branch = request.args.get("branch", "")

    conn = sqlite3.connect("college.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT branch
        FROM students
        ORDER BY branch
    """)

    branches = [row["branch"] for row in cursor.fetchall()]

    if selected_branch:
        cursor.execute(
            "SELECT * FROM students WHERE branch = ?",
            (selected_branch,)
        )
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "filter.html",
        students=students,
        branches=branches,
        selected_branch=selected_branch
    )



@app.route("/students")
def students_page():
    conn = get_db()
    students =conn.execute('SELECT * FROM students ORDER BY ID DESC').fetchall()
    return  render_template("students.html",students=students)


@app.route("/students/<int:id>/tip")
def get_ai_tip(id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        flash("Student not found", "danger")
    

    prompt = f"""
    Student name: {student['name']}
    Branch: {student['branch']}
    Marks: {student['marks']}/100
    Attendance: {student['attendance']}%
    
    Give a study tip for this student based on their marks and branch.
    if the marks are below 40, suggest ways to improve their performance.
    if the marks are above 60, suggest to focus on the weak subjects and score better.
    if the marks are above 80, suggest to improve their performance take mock tests and work on weaker areas to increase their marks.
    if the marks are above 95, suggest  Excellent performance keep up your consistency and dedication.
    and encourage them to continue learning and practicing.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    tip = response.choices[0].message.content
    return render_template("detail.html", student=student, tip=tip)




@app.route("/students/<int:id>")
def student_detail(id):

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",  (id,) ).fetchone()
    print(student)
    conn.close()
    if student is None:
        flash("Student not found", "danger")
        return redirect(url_for("records"))

    return render_template( "detail.html", student=student  )

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if session.get('role') != 'admin':
        flash("Admins only! You do not have permission to add a student.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form["name"]
        roll_no = int(request.form["roll_no"])
        branch = request.form["branch"]
        attendance = request.form["attendance"]
        marks = int(request.form["marks"])


    
       #Add: handle photo upload
        file = request.files.get('photo')
        filename = 'default.png'  # Default photo
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    


        conn = get_db()
        conn.execute(
            """
            INSERT INTO students
            (name, roll_no, branch, attendance, marks, photo)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, roll_no, branch, attendance, marks, filename)
        )
        conn.commit()
        conn.close()

        flash(f"Student {name} added successfully!", "success")
        return redirect(url_for("records"))

    return render_template("add_student.html")


# EDIT - update by ID
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    if 'user_id' not in session:
        flash("Admins only! You do not have permission to edit a student.", "warning")
        return redirect(url_for("login"))

    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    if request.method == 'POST':

        name = request.form['name']
        roll_no = request.form['roll_no']
        branch = request.form['branch']
        attendance = request.form['attendance']
        marks = request.form['marks']

        # Handle photo upload
        file = request.files.get('photo')
        filename = student[6]  # Keep the existing photo if no new one is uploaded
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor.execute("""
            UPDATE students
            SET name=?, roll_no=?, branch=?, attendance=?, marks=?, photo=?
            WHERE id=?
        """, (name, roll_no, branch, attendance, marks, filename))

        conn.commit()
        conn.close()

        flash(f"{name}'s record updated successfully!", "success")

        return redirect(url_for('records'))

    conn.close()

    return render_template('edit_student.html', student=student)



@app.route('/records')
def records():    
    conn = get_db()
    students = conn.execute("""
        SELECT id, name, roll_no, branch, attendance, marks, photo
        FROM students
    """).fetchall()
    conn.close()
     
      
    return render_template('records.html', students=students)

@app.route('/delete/<int:id>')
def delete_student(id):
    if 'user_id' not in session:
        flash("Admins only! You do not have permission to delete a student.", "warning")
        return redirect(url_for("login"))
    conn = get_db()

    # Check student exists
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",(id,) ).fetchone()

    if student is None:
        flash("Student not found", "danger")
        conn.close()
        return redirect(url_for('records'))

    # Delete student
    conn.execute(
        "DELETE FROM students WHERE id = ?",(id,) )

    conn.commit()
    conn.close()

    flash("Student deleted successfully", "success")
    return redirect(url_for('records'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db()
        # Check if username already exists
        existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Username already exists!', 'danger')
            conn.close()
            return render_template('register.html')
        
        hashed = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed, 'student'))
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username =?', (username,)).fetchone()
        conn.close()

        if user:
            if check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['role'] = user[3]
                flash('Login Successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid Password', 'danger')
        else:
            flash('User not found', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/branches')
def subjects():
    conn = get_db()
    rows = conn.execute('''
        SELECT branch AS branch_name, COUNT(id) AS student_count
        FROM students
        GROUP BY branch
        ORDER BY branch
    ''').fetchall()
    conn.close()
    return render_template('branches.html', rows=rows)

init_db()    
if __name__ == "__main__":
    app.run(debug=True)
