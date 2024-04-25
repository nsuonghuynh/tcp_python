import os
import socket
import sys
import argparse

students = []

class Student:
    def __init__(self, id, lname, fname, score):
        self.id = id
        self.lname = lname
        self.fname = fname
        self.score = score

    def __str__(self):
        return f"ID: {self.id}, Last: {self.lname}, First: {self.fname}, Score: {self.score}\n"
    
def update_db():
    global students
    with open("db.txt", 'r') as file:
        for line in file:
            fields = line.strip().split(',')
            id = fields[0][4:]
            lname = fields[1][7:]
            fname = fields[2][8:]
            score = fields[3][8:]
            student = Student(id, lname, fname, score)
            students.append(student)
    return 0

def search_student(id):
    global students
    for student in students:
        if student.id == id:
            return student.__str__()
    return "Student not found."

def search_by_score(score):
    global students
    records = []
    for student in students:
        if int(student.score) > int(score):
            records.append(student.__str__())
    message = "".join(records)
    if len(message) == 0:
        message = "No student found with given minimum score."
    return message 
        
def display_db():
    global students
    records = []
    for student in students:
        records.append(student.__str__())
    message = "".join(records)
    if len(message) == 0:
        message = "Database empty."
    return message

def remove_field(id):
    global students
    for i, student in enumerate(students):
        if student.id == id:
            students.pop(i)
            with open("db.txt", 'w') as file: 
                for student in students:
                    file.write(student.__str__()) 
            return "Student #{student.id} removed."
    return "Student not found."

def case1(connection):
    global students

    # Receive student data from the client
    data = connection.recv(1024).decode()
    print("Received for case1:", data)

    items = data.split()

    id = items[1]
    for student in students:
        if student.id == id:
            return "Student ID already exists."
        
    lname = items[2]
    fname = items[3]
    score = items[4]
    
    new_student = Student(id, lname, fname, score)
    students.append(new_student)

    with open("db.txt", "a") as file:
        file.write(new_student.__str__())
    
    return "Added new student.\n"

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
    print("Received for case5:", data)
    items = data.split()
    return(remove_field(items[1]))

def exit_program(connection):
    print("Connection closed.")
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

    file_path = "./db.txt"
    if os.path.exists(file_path):
        update_db()
        print("Database updated from 'db.txt'.")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket
    server_address = (args.ip, args.port)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection', file=sys.stderr)
        connection, client_address = sock.accept()

        try:
            # Receive the data from client
            while True:
                
                data = connection.recv(1024).decode('utf-8')

                if data:
                    response = switch_case(data[0], connection)
                    connection.sendall(response.encode('utf-8'))

                    if data == '6':
                        break

        finally:
            # Clean up the connection
            connection.close()

# if __name__ == "__main__":
#     main()
            
main()