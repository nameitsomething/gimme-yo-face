from threading import Thread

class server:

        class worker(Thread):
            def __init__(self,sock:socket:):
                Thread.__init__(self)
                self.sock = sock


            def run(self):
                print("here")
                while True:
                    data = self.recv(1024).decode()



        def __init__(self):
            self.sock = socket()
            self.PORT = 12345

        def connect(self):
            self.sock.bind(("",self.PORT))
            self.sock.listen(3)

        def acceptNew(self):
            conn, addr = self.sock.accept()
            client = self.worker(conn)
            client.start()


serv = server()
serv.connect()
while True:
    serv.acceptNew()