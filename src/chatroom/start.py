# Gabriel Casciano - 06, 30, 2020
# SimpleChatroom

# Start up and run script for the client side of the chat room


from socket import socket
from tkinter import *
from src.client.login import Login
from src.client.user import User


root = Tk()  # the tkinter root object
flag = 0  # flag to indicate how the windows exited
sock = socket()  # create and init empty socket
login_gui = Login(root, sock)  # create and init the login gui
user_gui = None  # create but do not init the user gui
running = True  # running bool for runtime loop

if __name__ == '__main__':
    while running:
        flag = login_gui.get_flag()  # get the current status flag from the window
        if flag == 0:  # if the flag is 0 all is normal keep looping
            root.update()  # update main task
            root.update_idletasks()  # update idle tasks
        elif flag == 1:
            root.destroy()
            running = False
        else:
            running = False# if the flag is anything other than 0, stop
    if flag == 1:  # if the flag is set to 1 after the login window, we run the main program
        # Re-initialize all the variables as necessary
        running = True
        flag = 0
        root = Tk()
        
        user_gui = User(root, sock)
        user_gui.identify()
        root.bind_all('<Return>', user_gui.enter_button_command)
        while running:
            flag = user_gui.get_flag()  # get the current status flag from the window
            if flag == 0:  # Normal operation
                user_gui.msg_loop() #gets new messages it reievces and displays it
                root.update()
                root.update_idletasks()
            else:  # Anything other than 0, exit
                running = False