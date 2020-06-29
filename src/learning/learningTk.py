from tkinter import *
import cv2
import time

class gui:

    def __init__(self,tk:Tk): #fuctions always have (self) to say its in the class
        self.tk = tk
        self.img = None
        self.counter = 0

        self.vs = cv2.VideoCapture(0)

        tk.title("title") #title
        self.tk.geometry("300x500") #size
        self.tk.resizable(0,0) #limits window resizeablity 

        self.textEntry = Entry(tk) #makes text box
        self.textEntry.pack(side=TOP) #shows + places, it top left


        self.button1 = Button(tk, text ="enter", command =self.enterButton) #button, 
        # command makes it do the function when clicked
        self.button1.pack(side=TOP) #draws on screen
        

    def enterButton(self): #function for click on button
        print(self.textEntry.get()) #prints out whats in text box
        self.textEntry.delete(0,"end") #deletes textbox after click button

    def initCamera(self):
        self.vs.read()[1]
        time.sleep(1)
       

    def updateVideo(self):
        self.img = self.vs.read()[1]
        cv2.imshow("Demo win", self.img)
        cv2.waitKey(1) #gives time to buffer

    def enterButton(self):
        cv2.imwrite(f"{self.textEntry.get()}.png", self.img)



root = Tk() #create object
GUI = gui(root) #not sure 

while True:
    GUI.updateVideo() #updates vdeio
    root.update_idletasks() #update window
    root.update() #runs the thing