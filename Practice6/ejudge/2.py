def g(b):
    return b % 2==0
y = int(input())
x = map(int, input().split())

f = filter(g, x)
print(len(list(f)))