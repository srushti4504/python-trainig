from flask import Flask, redirect, render_template, request, url_for, flash
from database import get_db ,init_db
import sqlite3

app = Flask(__name__)
app.secret_key = "College Smart Portal"

students = [
    {"id": 1, "name": "Aarav", "branch": "Computer", "attendance": "92%", "marks": 85},
    {"id": 2, "name": "Priya", "branch": "Mechanical", "attendance": "88%", "marks": 78},
    {"id": 3, "name": "Rahul", "branch": "Electrical", "attendance": "95%", "marks": 90},
    {"id": 4, "name": "Sneha", "branch": "Civil", "attendance": "89%", "marks": 82},
    {"id": 5, "name": "Rohan", "branch": "Computer", "attendance": "97%", "marks": 91}
]

notices = [
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

    return render_template(  "home.html", students=students  )

@app.route("/notices")
def notices():
    return render_template("notices.html", notices=notices)

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
    students =conn.execute('SELECT * FORM students ORDER BY ID DESC').fetchall()
    return  render_template("students.html",students=students)



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
    if request.method == "POST":
        name = request.form["name"]
        roll_no = int(request.form["roll_no"])
        branch = request.form["branch"]
        attendance = request.form["attendance"]
        marks = int(request.form["marks"])

        conn = get_db()

        conn.execute(
            """
            INSERT INTO students
            (name, roll_no, branch, attendance, marks)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, roll_no, branch, attendance, marks)
        )

        conn.commit()
        conn.close()

        

        flash(f"Student {name} added successfully!", "success")
        return redirect(url_for("records"))
        
    return render_template("add_student.html")


# EDIT - update by ID
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

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

        cursor.execute("""
            UPDATE students
            SET name=?, roll_no=?, branch=?, attendance=?, marks=?
            WHERE id=?
        """, (name, roll_no, branch, attendance, marks, id))

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
        SELECT id, name, roll_no, branch, attendance, marks
        FROM students
    """).fetchall()
    conn.close()

    return render_template('records.html', students=students)

@app.route('/delete/<int:id>')
def delete_student(id):

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

if __name__ == "__main__":
    init_db
    app.run(debug=True)
