

x = input()
y = 1

for i in range(len(x)):
    if int(x[i])%2==0:
        y=1
    elif int(x[i])%2!=0:
        y=0
        break
if y==0:
    print("Not valid")
else:
    print("Valid")

