y = int(input())
x = map(int, input().split())
sum = 0
for i in x:
    if i!=0:
        sum += 1

print(sum)