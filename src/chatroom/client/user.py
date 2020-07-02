  
# Gabriel Casciano - 06, 30, 2020
# SimpleChatroom

from tkinter import *
from socket import socket,error
from threading import *


class User:

    class Worker(Thread):
        def __init__(self, queue: list, conn: socket):
            Thread.__init__(self)
            self.queue = queue
            self.running = True
            self.sock = conn
            self.send_msg =""

        def recv_loop(self):
            data = "" # data var

            try:
                data = self.sock.recv(2).decode()

                if data ==0x1: # recv message
                    data = int(self.sock.recv(2)) # recv message size
                    data = self.sock.recv(data).decode() # recv message
                    self.queue.append(data) # appends data to queue

                elif data == 0x2: #send message
                    data = str.encode(self.send_msg).__sizeof__() #gets message size
                    self.sock.sendall(data) #sends message size
                    data = str.encode(self.send_msg) #encodes message
                    self.sock.sendall(data) #sends message

                    self.send_msg = "" # sets send_msg to nothing, whichi is important

            except error as msg:
                pass
            except Exception as exc:
                pass

        def run(self):
            while self.running:
                self.recv_loop()
                self.send()

        def send(self):
            if self.send_msg != "":
                self.sock.sendall(bytes(0x1)) # tells server to prepare to recv

        def add_to_queue(self,msg): #called by gui
            self.send_msg = msg
            pass

        def start(self):
            pass
    
    def __init__(self, tk: Tk, conn: socket):
        self.queue = []
        self.length_of_queue = 10
        self.flag = 0
        self.sock = conn  # no need to connect this socket object because it already was in login
        self.username = ""
        self.worker = self.Worker(self.queue, self.sock)
        self.worker.start() #starts worker

        self.tk = tk
        tk.title("Chatroom - Main Window")
        tk.geometry("380x160")
        tk.resizable(0,0)

        self.message_variable = StringVar()

        self.left_frame = Frame(tk,width =300) #makes frame 
        self.right_frame = Frame(tk,width = 100)

        # packs in left frame
        self.message_label = Label(self.left_frame, textvariable=self.message_variable, wraplength=250, justify=LEFT,anchor=NW) #ancor starts on northwest.
        self.message_entry = Entry(self.left_frame)

        #  packs buttons into right frame
        self.enter_button = Button(self.right_frame, text="Enter", command=self.enter_button_command)
        self.clear_button = Button(self.right_frame, text="Clear", command =self.clear_button_command)
        self.logout_button = Button(self.right_frame, text="Log Out")

        self.message_variable.set("Hello my name is gabriel casciano \n this is a test")

        #pack left frame
        self.message_label.pack(side=TOP, fill=X)
        self.message_entry.pack(side=BOTTOM, fill=X)
        self.left_frame.place(x=5,y=5,width=275,height=150)
        # pack right frame
        self.enter_button.pack(side=BOTTOM,fill=X)
        self.clear_button.pack(side=BOTTOM, fill=X)
        self.logout_button.pack(side=BOTTOM,fill=X)
        self.right_frame.place(x=280,y=5,width=80,height=150)

    def enter_button_command(self): # click enter button
        self.worker.add_to_queue(self.username + ">" + self.message_entry.get()) #adds text to queue
        self.message_entry.delete(0,"end") # clears text box

    def clear_button_command(self): #click clear button
        #clears the thing
        self.message_entry.delete(0,"end")
        self.message_variable.set("")


    def logout_button(self):
        pass

    def identify(self):
        self.sock.sendall(0x3) # asks server who we are
        self.username = self.sock.recv(4).decode() #gets username


    def main_loop(self):
        #  begin main update loop
        self.message_variable.set("")

        for msg in self.queue:
            self.message_variable.set(self.message_variable.get() + "\n"+ msg)

        if self.queue.__len__() > self.length_of_queue: #makes sure only 10 messages show
            self.queue.pop() # pops off top (oldest) message

        pass

    def get_flag(self):
        return self.flag


if __name__ == '__main__':
    root = Tk()
    gui = User(root, socket())

    root.mainloop()