n = int(input())
d = dict(zip(input().split(), input().split()))
q = input()

print(d.get(q, "Not found"))