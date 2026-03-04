import re
x = input().strip()
y = input()
g = re.search(y, x)
if g :
    print("Yes")
else:
    print("No")