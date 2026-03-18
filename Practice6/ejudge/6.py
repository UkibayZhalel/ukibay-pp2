n = int(input())
s = list(map(int, input().split()))

if all(x >= 0 for x in s):
    print("Yes")
else:
    print("No")