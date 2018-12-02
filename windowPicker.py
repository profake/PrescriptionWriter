from tkinter import *
import os
def runfunc(master):
        #Colors and font
        itemFont = "calibri 14 bold"
        bgLight = '#990038'
        bgDark = '#670026'

        photo = PhotoImage(file = "logo.png")
        label = Label(master, image=photo, bg='#340012')
        label.photo = photo
        label.pack()

        #canvas test
        canvas = Canvas(master, width=1280, height=20, bg = "#340012", highlightthickness=0)
        canvas.pack()

        left = Frame(master, width = 807, height = 664, bg = bgLight)
        left.pack()

        title = Label(text="Start", font='Ubuntu 26 bold', bg=bgLight, fg='white')
        title.place(x=110, y=230)

        iAmA = Label(text="Manage", font='Ubuntu 20 bold', bg=bgLight, fg='white')
        iAmA.place(x=100, y=350)


        def goBack():
            master.destroy()
            os.system('python adminLoginWindow.py')

        def medicinePanel():
            master.destroy()
            os.system('python runMedicineWindow.py')
        def patientPanel():
            master.destroy()
            os.system('python runPatientWindow.py')
        def prescriptionPanel():
            master.destroy()
            os.system('python runPrescriptionWindow.py')

        arrow = Button(master, text="Log out", width = 0, height=0, bg='white', command=goBack)
        arrow.place(x=0, y=0)

        userButton = Button(left, text="Medicine", width=10, height=1, bg="white", command=medicinePanel)
        userButton.place(x=60, y=220)

        adminButton = Button(left, text="Patients", width=10, height=1, bg="white", command=patientPanel)
        adminButton.place(x=180, y=220)

        prescButton = Button(left, text="Prescriptions", width=10, height=1, bg="white", command=prescriptionPanel)
        prescButton.place(x=120, y=280)

class initUI:
    def __init__(self, master):
        runfunc(master)
