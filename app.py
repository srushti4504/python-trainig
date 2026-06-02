from flask import  Flask

app = Flask(__name__)
#project data - dictionary
stud =[
    {"name":"srushti","marks":90,"course":"python"},
    {"name":"nandini","marks":85,"course":"python"},
    {"name":"priya","marks":95,"course":"python"},
    {"name":"Anuja","marks":80,"course":"python"}
]

@app.route("/")
def home():
    # Create using HTML
    html = "<h1>Collage Portal - students</h1>"
    html += "<ul>"
    for student in stud:
        html += f"<li>{student['name']} - {student['marks']} - {student['course']}</li>"
    html += "</ul>"
    return html


@app.route("/about")
def about():
    return '<h1>About Us</h1><p>This is a collage management system.</p>'
@app.route('/students')
def students():
    return '<h1>Students List</h1><p>This is the list of students</p>'
@app.route('/courses')
def courses():
    return '<h1>Courses</h1><p>This is the courses page.</p>'
if __name__ == "__main__":
    app.run(debug=True)