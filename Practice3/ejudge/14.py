n = int(input())
arr = list(map(int, input().split()))
q = int(input())

for _ in range(q):
    parts = input().split()

    if parts[0] == "add":
        x = int(parts[1])
        arr = list(map(lambda a: a + x, arr))

    elif parts[0] == "multiply":
        x = int(parts[1])
        arr = list(map(lambda a: a * x, arr))

    elif parts[0] == "power":
        x = int(parts[1])
        arr = list(map(lambda a: a ** x, arr))

    elif parts[0] == "abs":
        arr = list(map(lambda a: abs(a), arr))

print(*arr)
