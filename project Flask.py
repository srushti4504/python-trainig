from flask import Flask ,render_template

app = Flask(__name__)
students = [
    {"id": 1, "name": "Aarav", "branch": "Computer", "attendance": "92%", "marks": 85},
    {"id": 2, "name": "Priya", "branch": "Mechanical", "attendance": "88%", "marks": 78},
    {"id": 3, "name": "Rahul", "branch": "Electrical", "attendance": "95%", "marks": 90},
    {"id": 4, "name": "Sneha", "branch": "Civil", "attendance": "89%", "marks": 82},
    {"id": 5, "name": "Rohan", "branch": "Computer", "attendance": "97%", "marks": 91}
   ]

notices = [
    {    "Python Internship started on 28 May.",
         "Sir announced that",
         "To encourage learning, consistency, and active participation,"
         " a special competition has been announced.",
          "At the end of the training, "
          "the Top 5 performing students will be selected and rewarded with a special gift. "
    }
         ]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("records.html", students=students)

@app.route("/notices")
def notices():
    return render_template("notices.html", notices=notices)


if __name__ == "__main__":
    app.run(debug=True)
    