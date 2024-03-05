import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket
server_address = ('localhost', 8000)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection', file=sys.stderr)
    connection, client_address = sock.accept()

    try:
        
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            decoded_data = data.decode('utf-8')
            print(f'received "{decoded_data}"', file=sys.stderr)
            if data:
                print('sending data back to the client', file=sys.stderr)
                connection.sendall(data)
            else:
                print(f'no more data from {client_address}' , file=sys.stderr)
                break
            
    finally:
        # Clean up the connection
        connection.close()