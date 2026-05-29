name =input("Enter your name:")
marks =int(input("Enter your marks"))
percentage =float(input("Enter your percentage"))

print("/n -----Student Details -----")
print("Name:",name)
print("Marks:",marks)
print("Percentage:",percentage)

if marks>=75:
    print("(Student Name) has passed the exam")
elif marks>=60:
    print("(Student Name) has passed but improment")
else:
    print("(Student Name) has failed the exam")    