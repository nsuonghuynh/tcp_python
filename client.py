import socket
import sys


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8000)
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