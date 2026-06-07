import requests
import sys


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, y, x = extended_gcd(b % a, a)
        return gcd, x - (b // a) * y, y

def get_d(phi, e):
    gcd, x, y = extended_gcd(e, phi)
    
    if gcd != 1:
        raise ValueError("e and phi are not coprime; modular inverse does not exist.")
    else:
        # x might be negative, so we take it modulo phi to get the positive result
        return x % phi


if len(sys.argv) != 4:
    print("Usage: python3 rsa_breaker.py n e c.")
    print("n and e is the two keys from the public key. c is the cipher text")
    exit(1)

n = int(sys.argv[1])
e = int(sys.argv[2])
c = int(sys.argv[3])

response = requests.get(f"https://factordb.com/api?query={n}")
if response.status_code != 200:
    print("request fo p, q get error")
    exit(1)

response_body = response.json()
if response_body['status'] != 'FF':
    print(f"Search for FF status but get - {response_body['status']} status")
    exit(0)

factorize = response_body['factors']
if len(factorize) > 2 or sum(f[1] for f in factorize) > 2:
    print(f"There are more than two factors in your n - {factorize}.")

p, q = int(factorize[0][0]), int(factorize[1][0])
phi = (p - 1)*(q - 1)
d = get_d(phi, e)
bin_message = pow(c, d, n)
byte_m_len = (bin_message.bit_length() + 7) // 8
byte_message = bin_message.to_bytes(byte_m_len, byteorder='little') # if its look in reverse order try 'big' instead 'littel'
decoded_message = byte_message.decode('utf-8')
print(f"Decrypted text - \n{decoded_message}")
