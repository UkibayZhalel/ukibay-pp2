import re
x = input().strip()
y = input()
g = re.findall(y, x)
print(len(g))