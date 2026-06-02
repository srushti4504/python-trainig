students = ["srushti", "Sneha", "priya", "Pooja"]
marks = [85, 92, 78, 88]
attendance = [95, 98, 90, 96]

notices = [
    "Python Internship started on 28th May 2026.",
    "Every student has selected a project for practice.",
    "Students will work on their chosen project during the internship.",
    "By working on the project day by day, students will learn Python concepts and improve their programming skills.",
    "The project will help students gain practical experience and build confidence in coding."
]


def student_login():
    name = input("Enter Student Name: ")

    for i in range(len(students)):
        if students[i] == name:

            print("Login Successful")

            print("--- Student Details ---")
            print("Name:", name)
            print("Marks:", marks[i])
            print("Attendance:", attendance[i], "%")

            print("--- Notice Board ---")
            for notice in notices:
                print("*", notice)

            return

    print("Student Not Found")

student_login()