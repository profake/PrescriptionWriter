from tkinter import *
import adminLogin

#tk main window
admin = Tk()
x = adminLogin.initUI(admin)


#config root (main) window
admin.geometry("320x580+500+100")
admin.configure(background='#340012')
admin.resizable(False, False)
admin.wm_title("Login screen")

#Run program
admin.mainloop()
#-----------------
