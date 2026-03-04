import re

x = input().strip()

if re.match(r'^[a-zA-Z].*[0-9]$', x):
    print("Yes")
else:
    print("No")