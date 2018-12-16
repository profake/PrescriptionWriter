from tkinter import *
import prescription

#tk main window
start = Tk()
x = prescription.initUI(start)

#config root (main) window
start.geometry("1280x668+0+0")
start.configure(background='#2b2b2b')
start.resizable(False, False)
start.wm_title("Prescription Writer")

#Run program
start.mainloop()
#-----------------
