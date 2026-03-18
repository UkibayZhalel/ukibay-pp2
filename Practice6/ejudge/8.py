x = int(input())
y = set(list(map(int, input().split())))
g = sorted(y)
print(*g)