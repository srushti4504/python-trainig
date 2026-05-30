student = ["srushti", "ananya", "riya","sneha","priya"]
marks =[92,85,89,78,81]

def get_status(name,mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return  "B"
    elif mark >= 70:    
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"
for i in range (len(student)):
    grade = get_status(student[i],marks[i])
    print(f"{student[i]}: scored {marks[i]} and got grade {grade}")
