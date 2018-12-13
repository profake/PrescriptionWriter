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
        #canvas = Canvas(master, width=1280, height=20, bg = "#340012", highlightthickness=0)
        #canvas.pack()

        left = Frame(master, width=807, height=64, bg = bgLight)
        left.pack()

        bottomFrame = Frame(master, width=807, height=644, bg = bgLight)
        bottomFrame.place(x=0, y=200)

        medLabel = Label(text="Manage\nMedicine", font='Ubuntu 18 bold', bg=bgLight, fg='white')
        medLabel.place(x=80, y=400)

        patientLabel = Label(text="Manage\nPatients", font='Ubuntu 18 bold', bg=bgLight, fg='white')
        patientLabel.place(x=340, y=400)

        prescLabel = Label(text="Manage\nPrescriptions", font='Ubuntu 18 bold', bg=bgLight, fg='white')
        prescLabel.place(x=550, y=400)


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

        medButton = Button(bottomFrame, bg=bgLight, bd=0, command=medicinePanel)
        medButton.place(x=90, y=50)
        medImage= PhotoImage(file = 'medicine.png')
        medButton.config(image=medImage, compound=RIGHT)
        medButton.image = medImage

        patientButton = Button(bottomFrame, bg=bgLight, bd=0, command=patientPanel)
        patientButton.place(x=330, y=50)
        patientImage= PhotoImage(file = 'patient.png')
        patientButton.config(image=patientImage, compound=RIGHT)
        patientButton.image = patientImage

        prescriptionButton = Button(bottomFrame, bg=bgLight, bd=0, command=prescriptionPanel)
        prescriptionButton.place(x=580, y=50)
        prescriptionImage= PhotoImage(file = 'prescription.png')
        prescriptionButton.config(image=prescriptionImage, compound=RIGHT)
        prescriptionButton.image = prescriptionImage

class initUI:
    def __init__(self, master):
        runfunc(master)
