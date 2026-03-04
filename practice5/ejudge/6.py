import re

x = input().strip()
g = re.search(r'\S+@\S+\.\S+', x)
if g:
    print(g.group())
else:
    print("No email")