import socket
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip", "-i", type=str, default='localhost',help="Server IP")
parser.add_argument("--port", "-p", type=int, default=8000, help="Server port")
args = parser.parse_args()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket
# server_address = ('localhost', 8000)
server_address = (args.ip, args.port)
sock.connect(server_address)

try:
    
    # Send data
    message = 'This is the message.  It will be repeated.'
    print(f'sending "{message}"', file=sys.stderr)
    encoded_message = message.encode('utf-8')
    sock.sendall(encoded_message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print(f'received "{data}"', file=sys.stderr)

finally:
    print('closing socket', file=sys.stderr)
    sock.close()