import socket
import sys
import argparse


def menu():
    print("Menu")
    print("1. Add new student")
    print("2. Display Sudent Details by ID")
    print("3. Display Student Details by Score")
    print("4. Display All Student Data")
    print("5. Delete Student Details")
    print("6. Exit")
    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", "-i", type=str, default='localhost',help="Server IP")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Server port")
    args = parser.parse_args()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket
    server_address = ('localhost', 8000)

    # server_address = (args.ip, args.port)
    sock.connect(server_address)

    try:
        while True:
            # Print out menu
            menu()
            choice = input("Enter your choice: ")
            if (choice == '6'):
                message = choice
                print(f'Sending "{message}"', file=sys.stderr)
                encoded_message = message.encode('utf-8')
                sock.sendall(encoded_message)
                exit()

            elif (choice == '1'):

                id = input("Enter student ID: ")
                lname = input("Enter student last name:")
                fname = input("Enter student first name:")
                score = input("Enter student score:")

                items = [choice, id, lname, fname, score]
                message = " ".join(items)

                print(f'Sending "{message}"', file=sys.stderr)
                encoded_message = message.encode('utf-8')
                sock.sendall(encoded_message)
            
            elif (choice == '2'):

                id = input("Enter student ID: ")
                message = " ".join([choice, id])
                
                print(f'Sending "{message}"', file=sys.stderr)
                encoded_message = message.encode('utf-8')
                sock.sendall(encoded_message)

            elif (choice == '3'):
                
                score = input("Enter baseline score: ")
                message = " ".join([choice, score])

                print(f'Sending "{message}"', file=sys.stderr)
                encoded_message = message.encode('utf-8')
                sock.sendall(encoded_message)
            
            elif (choice == '4'):
                message = choice
                print(f'Sending "{message}"', file=sys.stderr)
                encoded_message = message.encode('utf-8')
                sock.sendall(encoded_message)

            elif (choice == '5'):
                id = input("Enter student ID: ")
                message = " ".join([choice, id])
                
                print(f'Sending "{message}"', file=sys.stderr)
                encoded_message = message.encode('utf-8')
                sock.sendall(encoded_message)

            # Send data
            # message = choice
            print(f'Sending "{message}"', file=sys.stderr)
            encoded_message = message.encode('utf-8')
            sock.sendall(encoded_message)

            # Look for amount received
            data = sock.recv(1024)
            print(f'Received "{data.decode('utf-8')}"', file=sys.stderr)

            # # Look for the response
            # amount_received = 0
            # amount_expected = len(message)
            
            # while amount_received < amount_expected:
            #     data = sock.recv(16)
            #     amount_received += len(data)
            #     print(f'received "{data}"', file=sys.stderr)

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()

if __name__ == '__main__':
    main()
