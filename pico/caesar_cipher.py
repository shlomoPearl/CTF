import sys

text = list(sys.argv[1])
for offset in range(1,26):
    for i, c in enumerate(text):
        if not c.isalpha(): continue
        first_ch = ord('a') if c.islower() else ord('A') 
        text[i] = chr(((ord(c) + 1 - first_ch) % 26) + first_ch)
    print("".join(text), offset)
