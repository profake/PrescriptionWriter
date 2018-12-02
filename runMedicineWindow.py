from tkinter import *
import medicine

root = Tk()
x = medicine.initUI(root)

root.geometry("960x768")
root.configure(background = 'orange')
root.resizable(False, False)
root.wm_title("Medicine Database")

root.mainloop()