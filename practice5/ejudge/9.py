x = list(input().split())
count = 0
for i in x:
    if len(i) == 3:
        count += 1
print(count)