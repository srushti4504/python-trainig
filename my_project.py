college_info = {
    "college_name": "Goverment polytechic Hingoli",
    "portal_name": "College Smart Portal",
    "city": "Hingoli, Maharashtra",
    "established_year": 2009
}

students = [
    {"id": 101, "name": "Srushti", "marks": 85, "attendance": 92},
    {"id": 102, "name": "Rahul", "marks": 72, "attendance": 88},
    {"id": 103, "name": "Priya", "marks": 58, "attendance": 80},
    {"id": 104, "name": "Amit", "marks": 42, "attendance": 75},
    {"id": 105, "name": "Sneha", "marks": 91, "attendance": 95}
]

def get_status(marks):
    if marks >= 75:
        return "Distinction"
    elif marks >= 60:
        return "First Class"
    elif marks >= 45:
        return "Pass"
    else:
        return "Fail"

print("===== COLLEGE SMART PORTAL =====")
for key, value in college_info.items():
    print(key, ":", value)

print("===== STUDENT RECORDS =====")

for student in students:
    print("ID:", student["id"])
    print("Name:", student["name"])
    print("Marks:", student["marks"])
    print("Attendance:", student["attendance"])
    print("Status:", get_status(student["marks"]))
    print("-" * 30)

notice_board = {
    "notice_id": 1,
    "title": "Python Internship",
    "date": "28-05-2026",
    "department": "Computer",
    "status": "Active"
}

print("===== NOTICE BOARD =====")
for key, value in notice_board.items():
    print(key, ":", value)

