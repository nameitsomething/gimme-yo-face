from socket import socket

class client:

    def __init__(self,HOST,PORT,username):
        self.sock =socket() #empty socket pocket
        self.HOST = HOST
        self.PORT = PORT
        self.msg = ""
        self.last_msg = ""
        self.username = username
        self.flag = False
        self.counter =0

    def connect(self):
        self.sock.connect((self.HOST,self.PORT))

    
    def close(self):
        self.sock.close()
        pass

    def runtime(self):
        self.counter +=1
        self.sock.sendall(str.encode(f"hello {self.counter}"))
        data=self.sock.recv(1024)
        print(data.decode())

    
cli = client("ec2-3-21-205-199.us-east-2.compute.amazonaws.com", 12345, "GABEC2")
cli.connect()

while True:
    cli.runtime()

        