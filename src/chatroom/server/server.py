from socket import *
from threading import *
import csv

HOST = ""
PORT = 12345

running = True
main_sock = socket()
clients = []


class Session(Thread):

    def __init__(self, conn:socket):
        Thread.__init__(self)
        self.data =""
        self.command = 0
        self.sock = conn
        self.recv_flag = False
        self.running = True
        self.username = ""



    def recv_loop(self):
        self.sock.settimeout(0.5) #wait time less, 
        try:
            if self.command == 1: #send data command
                # only issues by the server
                data = str.encode(self,data)
                self.sock.sendall(bytes(self.command))
                self.sock.sendall(bytes(data.__len__()))
                self.sock.sendall(data)
                self.command = 0

            elif self.command == 2: #recv data command
                # only issued by the client to the host
                self.sock.sendall(bytes(self.command))
                data = int(self.sock.recv(2))
                self.data = self.rock.recv(data).decode()
                self.recv_flag = True
                
                self.command = 0

            elif self.command == 3:
                if self.username is not "":
                    self.sock.sendall(str.encode(self.username))

                self.command = 0

            if self.command == 0:# wait for user ot issue a command
                self.command = int(self.sock.recv(2))

        except timeout as timeExcp:
            pass
        except error as errMsg:
            pass
        except Exception as exc:
            # anything else
            pass



def login(self): # check username/password
    creds = []
    with open('maybePasswords.csv', "r", newline=' ') as file:
        reader = reader.csv(file, delimiter=',')

        for row in reader:
            creds.append(row)

    data = self.sock.recv(256).decode().spilt(',')

    if data in creds: # if right
        self.sock.sendall(bytes(1)) #right passowrds
        self.username = data[0] 
        print("yeet")
        return True
    else: #if wrong
        self.sock.sendall(bytes(3)) #incrorect thing
        print("oof")
        return False



def run(self):
    if self.login():
        while self.running:
            self.recv_loop()



class Router(Thread): #router thread
    def __init__(self,conn:socket):
        self.sock = conn
        self.sock.listen()
        self.running = True

    def run(self):
        while self.running:
            conn,addr = self.sock.accept()
            session = Session(conn) #session is mirror version of user thats on server
            if session not in clients: #if session not in client list, add it
                session.start()
                clients.append(session)




def runtime():
    data=[]
    for c in clients:
        if c.recv_flag: # someone sent data
            data.append(c.data) #copy and break
            c.recv_flag = False # set flag to false

    for d in data:
        if d is not "":
            for c in clients: #send data to all
                c.command = 1
                c.data = data




if __name__ == '__main__':
    main_sock.bind((HOST,PORT))
    router = Router(main_sock)
    router.start()

    while running:
        runtime()

    router.running = False
    router.join()
