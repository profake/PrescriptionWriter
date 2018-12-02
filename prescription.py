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

def runfunc(master):
        #Colors and font
        itemFont = "calibri 14 bold"
        bgLight = '#f44242'
        bgDark = '#b72d2d'

        #canvas test
        canvas = Canvas(master, width=1280, height=50, bg = "orange", highlightthickness=0)
        canvas.pack()

        #Left panel
        left = Frame(master, width = 807, height = 664, bg = bgLight)
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


            problemLabel.place(x=10, y=200)

        tkvar.trace('w', change_dropdown)

        def returnToPicker():
            master.destroy()
            os.system('python windowPickerStarter.py')

class initUI:
    def __init__(self, master):
        runfunc(master)
