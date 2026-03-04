import re
x = input().strip()
g = re.findall("[0-9]", x)
print(*g)