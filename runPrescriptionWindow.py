from tkinter import *
import prescription

#tk main window
start = Tk()
x = prescription.initUI(start)

#config root (main) window
start.geometry("850x768")
start.configure(background='#340012')
start.resizable(False, False)
start.wm_title("Prescription Writer")

#Run program
start.mainloop()
#-----------------
