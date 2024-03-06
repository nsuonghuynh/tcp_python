import socket
import sys
import argparse

student_list = []

class Student:
    def __init__(self, id, lname, fname, score):
        self.id = id
        self.lname = lname
        self.fname = fname
        self.score = score

    def __str__(self):
        return f"ID: {self.id}, Last: {self.lname}, First: {self.fname}, Score: {self.score}\n"
    
    def update_id(self, new_id):
        self.id = new_id

    def update_lname(self, new_lname):
        self.lname = new_lname
    
    def update_fname(self, new_fname):
        self.fname = new_fname

    def update_score(self, new_score):
        self.score = new_score

def search_student(id):
    with open("db.txt", 'r') as file:
        for line in file:
            fields = line.strip().split(',')
            if fields[0][-6:] == id:
                return line
    return "Student not found"

def search_by_score(score):
    with open("db.txt", 'r') as file:
        records = []
        for line in file:
            fields = line.strip().split(',')
            scr = int(fields[3][7:])
            if (scr > int(score)):
                records.append(line)
        message = "".join(records)
        return message
        
def display_db():
    with open("db.txt", 'r') as file:
        records = []
        for line in file:
            records.append(line)
        message = " ".join(records)
        return message

def remove_field(id):
    lines = []
    with open("db.txt", 'r') as file:
        for line in file:
            fields = line.strip().split(',')
            if (fields[0][-6:] != id):
                lines.append(line)
    
    with open("db.txt", 'w') as file: 
        for line in lines:
            file.write(line) 
    return 0

def case1(connection):

    # Receive student data from the client
    data = connection.recv(1024).decode()
    print("Received for case1:", data)

    items = data.split()

    id = items[1]
    lname = items[2]
    fname = items[3]
    score = items[4]
    
    new_student = Student(id, lname, fname, score)
    student_list.append(new_student)

    with open("db.txt", "a") as file:
        file.write(new_student.__str__())
    
    return "Added new student\n"

def case2(connection):
    data = connection.recv(1024).decode()
    print("Received for case2:", data)
    items = data.split()
    return search_student(items[1])

def case3(connection):
    data = connection.recv(1024).decode()
    print("Received for case3:", data)
    items = data.split()
    return search_by_score(items[1])

def case4(connection):
    data = connection.recv(1024).decode()
    print("Received for case4:", data)
    return display_db()

def case5(connection):
    data = connection.recv(1024).decode()
    print("Received for case4:", data)
    items = data.split()
    remove_field(items[1])
    return "Student(s) not found or removed."

def exit_program(connection):
    exit()

def switch_case(choice, connection):
    switcher = {
        '1': case1,
        '2': case2,
        '3': case3,
        '4': case4,
        '5': case5,
        '6': exit_program
    }
    func = switcher.get(choice, lambda: "Invalid choice")
    return func(connection)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", "-i", type=str, default='localhost',help="Server IP")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Server port")
    args = parser.parse_args()


    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket
    # server_address = ('localhost', 8000)
    server_address = (args.ip, args.port)

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
                
                data = connection.recv(1024).decode('utf-8')

                print(data)

                if data:
                    response = switch_case(data[0], connection)
                    connection.sendall(response.encode('utf-8'))

                    if data == '6':
                        break
                    
                # print(f'Received "{decoded_data}"', file=sys.stderr)
                # if data:
                #     print('sending data back to the client', file=sys.stderr)
                #     connection.sendall(data)
                # else:
                #     print(f'No more data from {client_address}' , file=sys.stderr)
                #     break
                
        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
    main()