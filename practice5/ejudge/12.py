import re

x = input().strip()
y = re.findall(r'\d{2,}', x)
print(*y)