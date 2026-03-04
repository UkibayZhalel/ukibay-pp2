import re

x = input().strip()
y = input()
x = re.split(y, x)

for i in range(len(x)-1):
    print(x[i],end=",")

print(x[len(x)-1])