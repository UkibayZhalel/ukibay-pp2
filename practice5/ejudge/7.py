import re

x = input().strip()
y = input()
z = input()
x = re.sub(y, z, x)

print(x)