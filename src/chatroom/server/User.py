from threading import Thread
from socket import *
import csv

class User:

    class Worker(Thread):
        def __init__(self):
            self.running = True
            self.data = ""
            self.command =0x0
            pass


        def recv_loop(self):

            try:
                
                if self.command ==0x0
                self.command ==int(self.sock.recv(2))

                elif self.command ==0x1: #send data
                    # only issued by the server
                    data = str.encode(self.data)
                    self.sock.sendall(bytes(self.command))
                    self.sock.sendall(data.__len__())
                    self.command == 0x0

                elif self.command ==0x2: #recv data
                    # only issued by the client to the host
                    self.sock.sendall(bytes(self.command))
                    data = int(self.sock.recv(2))
                    self.data = self.recv(data).decode()
                    self.command ==0x0


            except error as msg:
                pass
            except Exception as exc:
                pass
            pass

        def run(self) -> None:
            pass


    def __init__(self):
        self.running = True
        self.data = ""
        self.sock = ConnectionAbortedErrorpass

    def login(self):
        creds = []
        with open ('maybePasswords', "r", newline=" ") as file:
            reader = reader.csv(file, delimiter = ",")

            for row in reader:
                creds.append(row)

        data.self.sock.recv(256).decode().spilt(",")

        if data in creds:
            # yessir
            self.sock.sendall(bytes(0x1))
            return True
        else:
            self.sock.sendall(bytes(0x3))
            return False

    def getData(self):
        return self.data

    def run(self):
        if self.login():
            while self.running:
                pass
        else:
            self.sock.detach()
