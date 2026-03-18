s = input()

vowels = "aeiouAEIOU"

if any(c in vowels for c in s) == True :
    print("Yes")
else:
    print("No")