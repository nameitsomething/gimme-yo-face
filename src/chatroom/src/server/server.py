import struct
from socket import *
from threading import *
import csv

HOST = ""
PORT = 12345

running = True
main_sock = socket()
clients = []


class Session(Thread):

    def __init__(self, conn: socket):
        Thread.__init__(self)
        self.data = ""
        self.command = 0
        self.sock = conn
        self.recv_flag = False
        self.running = True
        self.username = ""

    def recv_loop(self):
        self.sock.settimeout(0.5)
        try:
            if self.command == 1:  # send data command
                # only issues by the server
                data = str.encode(self.data)
                self.sock.sendall(struct.pack("B", self.command))
                self.sock.sendall(struct.pack("B", data.__len__()))
                self.sock.sendall(data)
                self.command = 0
                print(" server sent message, command 1")

            elif self.command == 2:  # recv data command
                # only issued by the client to the host
                self.sock.sendall(struct.pack("B", self.command))
                data = int.from_bytes(self.sock.recv(2) , "big")
                self.data = self.sock.recv(data).decode()
                
                self.recv_flag = True
                print(" server recieve message, command 2")
                self.command = 0

            elif self.command == 3:
                if self.username is not "":
                    self.sock.sendall(str.encode(self.username))
                    print("sends username")

                self.command = 0
                print("command 3 was done")

            if self.command == 0:  # wait for user to issue a command
                self.command = int.from_bytes(self.sock.recv(2), "big")
                print("server reiceved command")

        except timeout as timeExcp:
            print("timeout error?")
            pass
        except error as errMsg:
            print("error error?")
            pass

        except Exception as exc:
            print("green excepion error thing")
            # anything else
            pass

    def login(self):
        creds = []
        with open('maybePasswords.csv', "r", newline='') as file:
            reader = csv.reader(file, delimiter=',')

            for row in reader:
                creds.append(row)

        data = self.sock.recv(256).decode().split(',')

        if data in creds:
            self.sock.sendall(struct.pack("B", 1))
            self.username = data[0]
            print("correct password")
            return True
        else:
            self.sock.sendall(struct.pack("B", 2))
            print("wrong password/something else")
            return False

    def run(self):
        if self.login():
            while self.running:
                self.recv_loop()
                print("doing the recieve loop")


class Router(Thread):
    def __init__(self, conn: socket):
        Thread.__init__(self)
        self.sock = conn
        self.sock.listen()
        self.running = True

    def run(self):
        while self.running:
            conn, addr = self.sock.accept()
            session = Session(conn)
            if session not in clients: #session is mirror version of user that's on server
                #if the session doesn't exist, add it on to clients list
                session.start()
                clients.append(session) 
                print("added new session")
                


def runtime():
    data = []
    for c in clients:
        if c.recv_flag:  # someone has sent data
            data.append(c.data)  # copy and break
            c.recv_flag = False # reset the flag
            print("data was sent and flag has been reset")

    for d in data:
        if d is not "":
            for c in clients:  # send data to all
                c.command = 1
                c.data = data
                print("doing the sending thing")


if __name__ == '__main__':
    main_sock.bind((HOST, PORT))
    router = Router(main_sock)
    router.start()

    while running:
        runtime()

    router.running = False
    router.join()