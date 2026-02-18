data = input().split()

role = data[0]
name = data[1]
base_salary = int(data[2])

if role == "Manager":
    bonus_percent = int(data[3])
    total = base_salary + (base_salary * bonus_percent / 100)

elif role == "Developer":
    completed_projects = int(data[3])
    total = base_salary + (completed_projects * 500)

elif role == "Intern":
    total = base_salary

print(f"Name: {name}, Total: {total:.2f}")
