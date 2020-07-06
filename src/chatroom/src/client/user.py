from tkinter import *
from socket import socket, error, timeout
from threading import *


class User:
    class Worker(Thread):
        def __init__(self, conn: socket,):
            Thread.__init__(self)
            self.running = True
            self.sock = conn
            self.send_msg = ""
            

        def recv_loop(self):
            data = ""
            self.sock.settimeout(0.5)
            try:
                data = self.sock.recv(2).decode()

                if data == 1: # recv a msg
                    data = int(self.sock.recv(2)) # recv msg size
                    data = self.sock.recv(data).decode() # recv msg
                    self.queue.append(data) # append to queue
                    print("user recieve message")

                elif data == 2: # send a msg
                    data = str.encode(self.send_msg).__sizeof__() #send msg size
                    self.sock.sendall(bytes(data))
                    data = str.encode(self.send_msg)
                    self.sock.sendall(data)

                    self.send_msg = ""
                    print("user send message")
                else:
                    pass

            except timeout as time:
                pass
            except error as msg:
                pass
            except Exception as exc:
                # anything else
                pass

        def msg_loop(self):
            # begin the main update loop

            current_string = self.message_variable.get()

            for msg in self.queue:
                current_string += "\n" + msg
                self.queue.pop()

                lines = int(current_string.split("\n").__len__())
                if lines > 5:
                    hold = current_string.split("\n")[1:lines]
                    current_string = ''.join(hold)
                    

                self.message_variable.set(current_string)


        def send(self):
            if self.send_msg != "":
                self.sock.sendall(bytes(1)) # tell the server to prep for recv

        def run(self):
            while self.running:
                self.recv_loop()
                self.send()
                self.msg_loop()

        def add_to_queue(self, msg):  # also called by gui
            self.send_msg = msg
            pass

    def __init__(self, tk: Tk, conn: socket):
        self.queue = []
        self.sock = conn  # no need to connect this socket object because it already was in login
        self.username = ""
        self.message_variable = StringVar()
        self.worker = self.Worker(self.sock)
        self.worker.start()

        self.tk = tk
        tk.title("Chatroom - Main Window")
        tk.geometry("350x160")
        tk.resizable(0,0)

        self.left_frame = Frame(tk)
        self.right_frame = Frame(tk)

        self.message_label = Label(self.left_frame, textvariable=self.message_variable, wraplength=250, justify=LEFT, anchor=NW)
        self.message_entry = Entry(self.left_frame)

        self.enter_button = Button(self.right_frame, text="Enter", command=self.enter_button_command)
        self.clear_button = Button(self.right_frame, text="Clear", command=self.clear_button_command)
        self.logout_button = Button(self.right_frame, text="Log Out", command=self.logout_button_command)

        self.message_variable.set("This is an empty chat window")

        # Pack the left frame
        self.message_label.pack(side=TOP, fill=X)
        self.message_entry.pack(side=BOTTOM, fill=X)
        self.left_frame.place(x=5, y=5, width=275, height=150)
        # Pack the right frame
        self.enter_button.pack(side=BOTTOM, fill=X)
        self.clear_button.pack(side=BOTTOM, fill=X)
        self.logout_button.pack(side=BOTTOM, fill=X)
        self.right_frame.place(x=285, y=5, width=60, height=150)

    def enter_button_command(self):
        self.worker.add_to_queue(self.username + ">" + self.message_entry.get())
        self.message_entry.delete(0, "end")

    def clear_button_command(self):
        self.message_entry.delete(0, "end")
        self.message_variable.set("")

    def logout_button_command(self):
        pass

    def identify(self):
        self.sock.sendall(3)  # ask the server who we are
        self.username = self.sock.recv(4).decode()
