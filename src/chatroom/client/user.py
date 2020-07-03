  
# Gabriel Casciano - 06, 30, 2020
# SimpleChatroom

from tkinter import *
from socket import socket,error
from threading import *
import struct


class User:

    class Worker(Thread):
        def __init__(self, queue: list, conn: socket, msg_var: StringVar):
            Thread.__init__(self)
            self.queue = queue
            self.running = True
            self.sock = conn
            self.send_msg =""
            self.message_variable = msg_var #message variable

        def recv_loop(self):
            data = "" # data var
            self.sock.settimeout(0.5) # wait 0.5 seconds

            try:
                data = self.sock.recv(2).decode()

                if data ==1: # recv message
                    data = int.from_bytes(self.sock.recv(2)) # recv message size
                    data = self.sock.recv(data).decode() # recv message
                    self.queue.append(data) # appends data to queue

                elif data == 2: #send message
                    data = str.encode(self.send_msg).__sizeof__() #gets message size
                    self.sock.sendall(data) #sends message size
                    data = str.encode(self.send_msg) #encodes message
                    self.sock.sendall(data) #sends message

                    self.send_msg = "" # sets send_msg to nothing, whichi is important

            except error as msg:
                pass
            except Exception as exc:
                pass

        def msg_loop(self):
            # begin the main update loop

            current_string =self.message_variable.get() #get what's on-screen

            for msg in self.queue:
                current_thread += "\n" + msg # add typed out line in queue
                lines = int.(current_string.split("\n").__len__())
                if lines > 5: #checking if length is longer that 5 lines
                    hold = current_string.split("\n")[1:4] # getting rid of top line to make space for new line
                    current_string = ''.join(hold)

                self.message_variable.set(current_string)
                self.queue.pop()


        def run(self):
            while self.running:
                self.recv_loop()
                self.send()
                self.msg_loop()

        def send(self):
            if self.send_msg != "": #if msg isn't nothing
                self.sock.sendall(struct.pack("B", 1)) # tells server to prepare to recv

        def add_to_queue(self,msg): #called by gui
            self.send_msg = msg
            pass

        def start(self):
            pass
    
    def __init__(self, tk: Tk, conn: socket):
        self.queue = []
        self.sock = conn  # no need to connect this socket object because it already was in login
        self.username = ""
        self.message_variable = StringVar()
        self.worker = self.Worker(self.queue, self.sock, self.message_variable)
        self.worker.start() #starts worker

        self.tk = tk #makes window
        tk.title("Chatroom - Main Window")
        tk.geometry("380x160")
        tk.resizable(0,0) #can't change window size

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
        self.sock.sendall(3) # asks server who we are
        self.username = self.sock.recv(4).decode() #gets username


    def main_loop(self):
        #  begin main update loop
        self.message_variable.set("")

        for msg in self.queue:
            self.message_variable.set(self.message_variable.get() + "\n"+ msg)

        if self.queue.__len__() > self.length_of_queue: #makes sure only 10 messages show
            self.queue.pop() # pops off top (oldest) message

        pass

if __name__ == '__main__':
    root = Tk()
    gui = User(root, socket())

    gui.identify()
    root.mainloop()
    gui.worker.join()