y = int(input())
x = map(str, input().split())

for i, v in enumerate(x):
    print(i,end=':')
    print(v,end=' ')