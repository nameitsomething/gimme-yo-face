# Gabriel Casciano - 06, 30, 2020
# SimpleChatroom

# Flag codes:
# 0 - Normal operation
# 1 - Normal Exit
# 2 - Error
# 3 - Incorrect Login creds


from tkinter import *
from socket import socket
from threading import *

HOST = "3.128.156.248"  # Host address
PORT = 12345  # Host port


class Login:
    def __init__(self, tk: Tk, conn: socket):
        self.flag = 0  # flag for exit code
        self.tk = tk  # tkinter root object
        self.sock = conn  # socket object

        tk.title("Chatroom - Login")  # set the window title

        self.username_entry = Entry(tk)  # create the username text entry
        self.password_entry = Entry(tk)  # create the password text entry
        self.login_button = Button(tk, text="Login", command=self.login_button)  # create the login button
        self.cancel_button = Button(tk, text="Cancel", command=self.cancel_button)  # create the cancel button

        # Set up the grid of text entries and buttons:
        self.username_entry.grid(row=0, column=0)
        self.login_button.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=0)
        self.cancel_button.grid(row=1, column=1)

    def login_button(self):  # When the login button is pressed, parse the text entries and login
        self.login(self.username_entry.get(), self.password_entry.get())

    def cancel_button(self):  # When then cancel button is pressed, clear the text entries
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

    def login(self, user: str, pw: str):  # Login in command, username and password as parameters
        self.sock.connect((HOST, PORT))  # First, connect to the server
        data = f"{user},{pw}"  # format login data to send to the server
        self.sock.sendall(data.encode())  # encode and send the data
        data = int.from_bytes(self.sock.recv(2), "big") # wait for a response on whether or not it was successful

        print(data)

        if data == 1:  # Normal login
            self.flag = 1  # set normal login flag
            print("Normal")
        elif data == 2:  # Incorrect creds
            self.flag = 3
            self.sock.detach()  # if login fails, disconnect from server
            print("Not Normal")
        else:
            self.flag = 2  # abnormal login
            print("not normal 2")
            self.sock.detach()

    def get_flag(self):  # get flag for external user
        return self.flag

    def create_user(self, user: str, pw: str):  # not implemented yet
        data = 0
        return data