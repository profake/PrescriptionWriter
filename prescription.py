from tkinter import *
import tkinter.messagebox
import sqlite3
import helpers
import tkinter.ttk as ttk
import tkinter.font as tkFont
import string
import os


medType = ""
medName = ""
dose = ""

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
                pass

        def adder():
            items_list = []
            items_list.extend([medName, medType, dose])
            dbtobox(items_list)

        def dropDownAdder():
            global ddPosY

            tkvar = StringVar(master)
            tkvar.set('Pick type..')  # set the default option
            medTypeMenu = OptionMenu(left, tkvar, *type_list)
            medTypeMenu.place(x=ddPosX, y=ddPosY)


            def change_dd(*args):
                global medType
                medType = tkvar.get()
                medType = medType.replace("'", "")
                medType = medType.replace(",", "")
                medType = medType.replace("(", "")
                medType = medType.replace(")", "")


                curM.execute("SELECT trade_name from medicine where type = ?", (medType,))
                medicine_list = []
                for row in curM.fetchall():
                    medicine_list.append(row)

                tkvar2 = StringVar(master)
                tkvar2.set('Pick medicine..')
                popupMenu2 = OptionMenu(left, tkvar2, *medicine_list)
                popupMenu2.place(x=ddPosX+140, y=ddPosY)

                def change_dd2(*args):
                    global medName
                    medName = tkvar2.get()
                    medName = medName.replace("'", "")
                    medName = medName.replace(",", "")
                    medName = medName.replace("(", "")
                    medName = medName.replace(")", "")

                tkvar2.trace('w', change_dd2)

                tkvar3 = StringVar(master)
                tkvar3.set('Pick dosage..')
                popupMenu3 = OptionMenu(left, tkvar3, "Once at morning", "Once at night", "Twice per day", "3 times per day")
                popupMenu3.place(x=ddPosX+300, y=ddPosY)

                def change_dd3(*args):
                    global dose
                    dose = tkvar3.get()
                    dose = dose.replace("'", "")
                    dose = dose.replace(",", "")
                    dose = dose.replace("(", "")
                    dose = dose.replace(")", "")

                tkvar3.trace('w', change_dd3)


            tkvar.trace('w', change_dd)

            printButton = Button(left, text="Print", width=10, height=1, bg="orange", command=printer)
            printButton.place(x=720, y=500)

            addButton = Button(left, text="Add", width=10, height=1, bg="orange", command=adder)
            addButton.place(x=620, y=500)

        def change_dropdown(*args):

            for i in tree.get_children():
                tree.delete(i)

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
