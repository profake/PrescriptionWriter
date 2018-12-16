from tkinter import *
import windowPicker
from tkinter.ttk import *

#tk main window
start = Tk()
x = windowPicker.initUI(start) #it's in a different file because its cluttered :@

#config root (main) window
start.geometry("800x580+250+100")
start.configure(background='#340012')
start.resizable(False, False)
start.wm_title("Prescription Writer")

#Run program
start.mainloop()
#-----------------
