from tkinter import *
import patient

root = Tk()
x = patient.presc(root)

root.geometry("1280x768+0+0")
root.configure(background = '#191919')
root.resizable(False, False)
root.wm_title("Prescription Writer")

root.mainloop()