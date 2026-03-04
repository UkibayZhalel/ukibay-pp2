import re

x = input().strip()
y = re.findall(r'[A-Z]', x)
print(len(y))