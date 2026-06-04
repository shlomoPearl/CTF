import base64
plaintext = b'{"showpassword":"no","bgcolor":"#ffffff"}'
cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg="

ciphertext = base64.b64decode(cookie)
key_stream = bytes(p ^ c for p, c in zip(plaintext, ciphertext))
print(key_stream)
print(type(key_stream))

inject_text = b'{"showpassword":"yes","bgcolor":"#ffffff"}'
key = key_stream[:4]
cookie_stream = bytes(b ^ key[i % len(key)] for i, b in enumerate(inject_text))
cookie = base64.b64encode(cookie_stream).decode()
print(cookie)
print(type(cookie))

