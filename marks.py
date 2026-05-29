sub1 = int(input("Enter marks for Subject 1: "))
sub2 = int(input("Enter marks for Subject 2: "))
sub3 = int(input("Enter marks for Subject 3: "))
sub4 = int(input("Enter marks for Subject 4: "))
sub5 = int(input("Enter marks for Subject 5: "))

total = sub1 + sub2 + sub3 + sub4 +sub5 
percentage =total /5
print("Total Marks =",total)
print ("Percentage =",percentage)
if percentage >= 75:
   print("Result:Distinction")
elif percentage >= 60:      
   print("Result:First class ")
elif percentage >= 45 :
   print ("Result : pass")
else:
   print("Result: fail")      