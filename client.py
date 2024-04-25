import socket
import sys
import argparse


def menu():
    print("\nMenu")
    print("1. Add New Student")
    print("2. Display Sudent Details by ID")
    print("3. Display Student Details by Minimum Score")
    print("4. Display All Student Data")
    print("5. Delete Student Record")
    print("6. Exit")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", "-i", type=str, default='localhost',help="Server IP")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Server port")
    args = parser.parse_args()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket
    server_address = (args.ip, args.port)
    sock.connect(server_address)

    try:
        while True:
            # Print out menu
            menu()
            choice = input("\nEnter your choice: ")

            if (choice == '6'):
                message = choice
                encoded_message = message.encode('utf-8')
                sock.sendall(encoded_message)
                exit()

            elif (choice == '1'):
                id = input("Enter 6-digit student ID: ")
                while (len(id) != 6 or id.isdigit() == False):
                    id = input("Invalid student ID.\n Please re-enter student ID: ")
                lname = input("Enter student last name: ")
                fname = input("Enter student first name: ")
                score = int(input("Enter student score: "))
                while (score < 0 or score > 100):
                    score = int(input("Score must be between 0 and 100: "))

                items = [choice, id, lname, fname, str(score)]
                message = " ".join(items)
            
            elif (choice == '2'):
                id = input("Enter student ID: ")
                while (len(id) != 6 or id.isdigit() == False):
                    id = input("Invalid student ID.\n Please re-enter student ID: ")
                message = " ".join([choice, id])

            elif (choice == '3'):
                score = int(input("Enter minimum score: "))
                while (score < 0 or score > 100):
                    score = int(input("Score must be between 0 and 100: "))
                message = " ".join([choice, str(score)])
            
            elif (choice == '4'):
                message = choice

            elif (choice == '5'):
                id = input("Enter student ID: ")
                while (len(id) != 6 or id.isdigit() == False):
                    id = input("Invalid student ID.\n Please re-enter student ID: ")
                message = " ".join([choice, id])

            # Send data
            encoded_message = message.encode('utf-8')
            sock.sendall(encoded_message)

            # message = choice
            print(f'Sending:\n {message}', file=sys.stderr)
            encoded_message = message.encode('utf-8')
            sock.sendall(encoded_message)

            # Look for response received
            data = sock.recv(1024)
            decoded_data = data.decode('utf-8')
            print(f'Received:\n{decoded_data}*End of messge*\n', file=sys.stderr)

    finally:
        print('Closing socket...\n', file=sys.stderr)
        sock.close()

# if __name__ == '__main__':
#     main()
        
main()
