from tkinter import *
import patient

root = Tk()
x = patient.presc(root)

root.geometry("1280x768+500+280")
root.configure(background = 'orange')
root.resizable(False, False)
root.wm_title("Prescription Writer")

root.mainloop()