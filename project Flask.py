from flask import Flask, redirect, render_template, request, url_for, flash
from database import get_db ,init_db

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


@app.route('/records')
def records():
    conn = get_db()
    students = conn.execute("""
        SELECT id, name, roll_no, branch, attendance, marks
        FROM students
    """).fetchall()
    conn.close()

    return render_template('records.html', students=students)


if __name__ == "__main__":
    init_db
    app.run(debug=True)
