from tkinter import *
import medicine

root = Tk()
x = medicine.initUI(root)

root.geometry("960x768+250+0")
root.configure(background = '#191919')
root.resizable(False, False)
root.wm_title("Medicine Database")

root.mainloop()