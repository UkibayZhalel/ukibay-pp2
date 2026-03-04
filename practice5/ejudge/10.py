import re
x = input().strip()
y = re.findall("cat", x)
z = re.findall("dog", x)
if (len(y) > 0) or (len(z) > 0):
    print("Yes")
else:
    print("No")