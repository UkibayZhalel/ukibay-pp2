import re
x = input()
y = re.match("Hello", x)
if y :
    print("Yes")
else:
    print("No")