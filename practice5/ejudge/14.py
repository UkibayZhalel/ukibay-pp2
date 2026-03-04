import re

text = input().strip()

pattern = re.compile(r'^\d+$')

if pattern.fullmatch(text):
    print("Match")
else:
    print("No match")