x =int(input())
while (x %2 ==0 or x % 3 ==0 or x % 5 ==0):
    if x % 2 == 0:
        x = x / 2
    elif x % 3 == 0:
        x = x / 3
    elif x % 5 == 0:
        x = x / 5

if x == 1:
    print("Yes")
else:
    print("No")