from tkinter import *
import tkinter.messagebox
import sqlite3
import helpers
import tkinter.ttk as ttk
import tkinter.font as tkFont
import string
import os

# db stuff
conn = sqlite3.connect('patient.db')
cur = conn.cursor()
cur.execute("SELECT client_name from log")
patient_list = []
for row in cur.fetchall():
    patient_list.append(row)

connM = sqlite3.connect('medicine_database.db')
curM = connM.cursor()
curM.execute("SELECT distinct type from medicine")
type_list = []
for row in curM.fetchall():
    type_list.append(row)

#dropdown pos x and y
ddPosX = 40
ddPosY = 180

def runfunc(master):
        #Colors and font
        itemFont = "calibri 14 bold"
        bgLight = '#f44242'
        bgDark = '#b72d2d'

        #canvas test
        canvas = Canvas(master, width=1280, height=50, bg = "orange", highlightthickness=0)
        canvas.pack()

        #Left panel
        left = Frame(master, width = 857, height = 664, bg = bgLight)
        left.pack(side = LEFT)

        title = Label(text="☇Prescription Writer", font='Ubuntu 26 bold', bg="orange", fg='white')
        title.place(x=0, y=0)

        tkvar = StringVar(master)

        tkvar.set('Pick patient..')  # set the default option
        popupMenu = OptionMenu(left, tkvar, *patient_list)
        popupMenu.place(x=345, y=10)

        # on change dropdown value

        patientName = Label(text="", font='Ubuntu 24 bold', bg="orange", fg='white')
        problemLabel = Label(text="Problem: ", font='Ubuntu 16 bold', bg="orange", fg="white")
        problemTextLabel = Label(text="", font='Ubuntu 16', bg="orange", fg="white")
        problemTextLabel.place(x=120, y=201)
        patientName.place(x=10, y=150)

        def printer():
            pass

        def dropDownAdder():
            global ddPosY

            tkvar = StringVar(master)
            tkvar.set('Pick type..')  # set the default option
            popupMenu = OptionMenu(left, tkvar, *type_list)
            popupMenu.place(x=ddPosX, y=ddPosY)


            def change_dd(*args):
                getName = tkvar.get()
                getName = getName.replace("'", "")
                getName = getName.replace(",", "")
                getName = getName.replace("(", "")
                getName = getName.replace(")", "")

                curM.execute("SELECT trade_name from medicine where type = ?", (getName,))
                medicine_list = []
                for row in curM.fetchall():
                    medicine_list.append(row)

                tkvar2 = StringVar(master)
                tkvar2.set('Pick medicine..')
                popupMenu2 = OptionMenu(left, tkvar2, *medicine_list)
                popupMenu2.place(x=ddPosX+140, y=ddPosY-40)

                tkvar3 = StringVar(master)
                tkvar3.set('Pick dosage..')
                popupMenu3 = OptionMenu(left, tkvar3, "Once at morning", "Once at night", "Twice per day", "3 times per day")
                popupMenu3.place(x=ddPosX+300, y=ddPosY-40)



            tkvar.trace('w', change_dd)

            ddPosY = 40 + ddPosY

            printButton = Button(left, text="Print", width=10, height=2, bg="orange", command=printer)
            printButton.place(x=720, y=500)

        def change_dropdown(*args):

            getName = tkvar.get()
            getName = getName.replace("'", "")
            getName = getName.replace(",", "")
            getName = getName.replace("(", "")
            getName = getName.replace(")", "")

            #Get problem
            cur.execute("SELECT problem FROM log WHERE client_name = ?", (getName,))
            data = cur.fetchall()
            actualProblem = data[0][0]

            patientName.configure(text=getName)
            patientName.update()

            problemTextLabel.configure(text=actualProblem)
            problemTextLabel.update()

            adderButton = Button(left, text="+", width=1, height=1, bg="orange", command=dropDownAdder)
            adderButton.place(x=720, y=180)

            problemLabel.place(x=10, y=200)

        tkvar.trace('w', change_dropdown)

        def returnToPicker():
            master.destroy()
            os.system('python windowPickerStarter.py')

        returnButton = Button(canvas, text="Return", width=10, height=1, bg="white", command=returnToPicker)
        returnButton.place(x=720, y=10)

class initUI:
    def __init__(self, master):
        runfunc(master)
