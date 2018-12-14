from tkinter import *
import tkinter.messagebox
import sqlite3
import helpers
import tkinter.ttk as ttk
import tkinter.font as tkFont
import string
import datetime
import os
now = datetime.datetime.now()

medType = ""
medName = ""
dose = ""

# db stuff
medicine_list = []

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
        bgLight = '#424242'
        bgDark = '#2b2b2b'

        #canvas test
        canvas = Canvas(master, width=1280, height=50, bg = "#2b2b2b", highlightthickness=0)
        canvas.pack()

        #Left panel
        left = Frame(master, width = 857, height = 664, bg = bgLight)
        left.pack(side = LEFT)

        title = Label(text="☇Prescription Writer", font='Ubuntu 26 bold', bg=bgDark, fg='white')
        title.place(x=0, y=0)

        tkvar = StringVar(master)

        tkvar.set('Pick patient..')  # set the default option
        popupMenu = OptionMenu(left, tkvar, *patient_list)
        popupMenu.place(x=345, y=10)

        # on change dropdown value

        patientName = Label(text="", font='Ubuntu 24 bold', bg=bgDark, fg='white')
        problemLabel = Label(text="Problem: ", font='Ubuntu 16 bold', bg=bgLight, fg="white")
        problemTextLabel = Label(text="", font='Ubuntu 16', bg=bgLight, fg="white")
        problemTextLabel.place(x=120, y=201)
        patientName.place(x=10, y=150)

        boxHeaders = ['Name', 'Company', 'Dosage']
        # --------------------------
        container = ttk.Frame(left)
        container.place(x=550, y=70)
        tree = ttk.Treeview(columns=boxHeaders, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(column=0, row=0, sticky='nsew', in_=container)

        def sortby(tree, col, descending):
            data = [(tree.set(child, col), child) \
                    for child in tree.get_children('')]
            data.sort(reverse=descending)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)
            tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

        def OnDoubleClick(ev):
            pass
            item = tree.focus()
            tree.delete(item)

        tree.bind("<Double-1>", OnDoubleClick)

        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        # --------------------------
        for col in boxHeaders:
            tree.heading(col, text=col,
                         command=lambda c=col: sortby(tree, c, 0))
            # adjust the column's width to the header string
            tree.column(col, width=90)

        def dbtobox(items_list):
            tree.insert('', 'end', values=items_list)
                # adjust column's width if necessary to fit each value
                #for ix, val in enumerate(item):
                    #col_w = tkFont.Font().measure(val)
                    #if tree.column(boxHeaders[ix], width=None) < col_w:
                        #tree.column(boxHeaders[ix], width=col_w)


        def printer():
            result = tkinter.messagebox.askquestion("Confirmation",
                                                    "Are you sure you want to print prescription?")
            if result == 'yes':
                c_name = tkvar.get()[2:-3]
                currentDate = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
                cur.execute(
                    "UPDATE log SET status = ?, last_visit = ? WHERE client_name = ?",
                    ("Done", currentDate, c_name))
                conn.commit()
        def adder():
            items_list = []
            items_list.extend([medName, medType, dose])
            dbtobox(items_list)

        tkvar1 = StringVar(master)
        tkvar1.set('Pick type..')  # set the default option
        medTypeMenu = OptionMenu(left, tkvar1, *type_list)

        tkvar2 = StringVar(master)
        tkvar2.set('Pick medicine..')

        tkvar3 = StringVar(master)
        tkvar3.set('Pick dosage..')
        dosageMenu = OptionMenu(left, tkvar3, "Once at morning", "Once at night", "Twice per day", "3 times per day")

        def dropDownAdder():
            global ddPosY

            medTypeMenu.place(x=ddPosX, y=ddPosY)

            def change_dd(*args):
                tkvar2.set("Pick medicine..")
                tkvar3.set("Pick dosage..")
                global medType
                global medicine_list

                medType = tkvar1.get()[2:-3]
                print(medType)
                curM.execute("SELECT trade_name from medicine where type = ?", (medType,))

                medicine_list.clear()
                for row in curM.fetchall():
                    medicine_list.append(row)

                medNameMenu = OptionMenu(left, tkvar2, *medicine_list)
                medNameMenu.place(x=ddPosX+140, y=ddPosY)

                def change_dd2(*args):
                    global medName
                    medName = tkvar2.get()[2:-3]

                tkvar2.trace('w', change_dd2)

                dosageMenu.place(x=ddPosX+300, y=ddPosY)

                def change_dd3(*args):
                    global dose
                    dose = tkvar3.get()

                tkvar3.trace('w', change_dd3)


            tkvar1.trace('w', change_dd)

            printButton = Button(left, text="Print", width=10, height=1, bg="orange", command=printer)
            printButton.place(x=720, y=500)

            addButton = Button(left, text="Add", width=10, height=1, bg="orange", command=adder)
            addButton.place(x=620, y=500)

        def change_dropdown(*args):

            for i in tree.get_children():
                tree.delete(i)

            getName = tkvar.get()[2:-3]

            #Get problem
            cur.execute("SELECT problem FROM log WHERE client_name = ?", (getName,))
            data = cur.fetchall()
            actualProblem = data[0][0]

            patientName.configure(text=getName)
            patientName.update()

            problemTextLabel.configure(text=actualProblem)
            problemTextLabel.update()

            problemLabel.place(x=10, y=200)

            dropDownAdder()

        tkvar.trace('w', change_dropdown)

        def returnToPicker():
            master.destroy()
            os.system('python windowPickerStarter.py')

        returnButton = Button(canvas, text="Return", width=10, height=1, bg="white", command=returnToPicker)
        returnButton.place(x=720, y=10)

class initUI:
    def __init__(self, master):
        runfunc(master)
