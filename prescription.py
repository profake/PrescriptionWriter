import datetime
import os
import sqlite3
import tkinter.messagebox
import tkinter.ttk as ttk
from tkinter import *
from fpdf import FPDF

now = datetime.datetime.now()

medType = ""
medName = ""
dose = ""
duration = ""

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

# dropdown pos x and y
ddPosX = 40
ddPosY = 200

def runfunc(master):
    # Colors and font
    itemFont = "calibri 14 bold"
    bgLight = '#424242'
    bgDark = '#2b2b2b'

    # canvas test
    canvas = Canvas(master, width=1280, height=50, bg="#2b2b2b", highlightthickness=0)
    canvas.pack()

    # Left panel
    left = Frame(master, width=1280, height=664, bg=bgLight)
    left.pack(side=LEFT)

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

    boxHeaders = ['Type', 'Name', 'Dosage', 'Course Duration']
    # --------------------------
    container = ttk.Frame(left)
    container.place(x=750, y=70)
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
        tree.column(col, width=110)

    def dbtobox(items_list):
        tree.insert('', 'end', values=items_list)
        # adjust column's width if necessary to fit each value
        # for ix, val in enumerate(item):
        # col_w = tkFont.Font().measure(val)
        # if tree.column(boxHeaders[ix], width=None) < col_w:
        # tree.column(boxHeaders[ix], width=col_w)

    def printer():
        result = tkinter.messagebox.askquestion("Confirmation",
                                                "Confirm prescription?")
        if result == 'yes':
            c_name = tkvar.get()[2:-3]
            currentDate = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
            cur.execute(
                "UPDATE log SET status = ?, last_visit = ? WHERE client_name = ?",
                ("Done", currentDate, c_name))
            conn.commit()
            tkinter.messagebox.showinfo("Information", "Prescription confirmed for " + c_name + ".")

            cur.execute("SELECT date_of_birth from log WHERE client_name = ?", (c_name,))
            patientAge = now.year - int(cur.fetchall()[0][0][6:])

            cur.execute("SELECT problem from log WHERE client_name = ?", (c_name,))
            diagnosis = cur.fetchall()[0][0]

            prescFileName = c_name + " " + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + ".pdf"

            pdf = FPDF()
            pdf.add_page()

            pdf.set_font("Helvetica", size=14)
            pdf.cell(10, 10, txt="Prescription for "+c_name, ln=1, align='L')
            pdf.set_font("Helvetica", size=12)
            pdf.cell(10, 10, txt="Age: "+str(patientAge), ln=1, align='L')
            pdf.cell(10, 10, txt="Date of visit: "+str(now.day)+"/"+str(now.month)+"/"+str(now.year), ln=1, align='L')
            pdf.cell(10, 10, txt="Diagnosis: "+diagnosis, ln=1, align='L')
            pdf.line(10, 10, 10, 50)
            pdf.set_line_width(1)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(20)

            pdf.cell(10, 10, txt="Medicine prescribed:", ln=1, align='L')
            pdf.set_line_width(0.2)
            col_width = pdf.w/4.5
            row_height=pdf.font_size

            pdf.cell(col_width, row_height*1.2, txt="Type", border=0)
            pdf.cell(col_width, row_height*1.2, txt="Name", border=0)
            pdf.cell(col_width, row_height*1.2, txt="Dosage", border=0)
            pdf.cell(col_width, row_height*1.2, txt="Duration", border=0)
            pdf.ln(10)

            for line in tree.get_children():
                for value in tree.item(line)['values']:
                    pdf.cell(col_width, row_height*1.2, txt=value, border=1)
                pdf.ln(row_height*1.4)

            pdf.ln(35)
            pdf.cell(50, 5, txt='-------------', ln=1, align='L')
            pdf.cell(50, 5, txt='Signature', ln=1, align='L')
            pdf.output(prescFileName)
            os.startfile(prescFileName, 'open')

    def adder():
        items_list = []
        items_list.extend([medType, medName, dose, duration])
        dbtobox(items_list)

    tkvar1 = StringVar(master)
    tkvar1.set('Pick type..')  # set the default option
    medTypeMenu = OptionMenu(left, tkvar1, *type_list)

    tkvar2 = StringVar(master)
    tkvar2.set('Pick medicine..')

    tkvar3 = StringVar(master)
    tkvar3.set('Pick dosage..')
    dosageMenu = OptionMenu(left, tkvar3, "Once at morning", "Once at night", "Twice per day", "3 times per day")

    tkvar4 = StringVar(master)
    tkvar4.set('Pick course duration..')
    durationMenu = OptionMenu(left, tkvar4, "3 days", "7 days", "10 days", "15 days", "One month", "Three months",
                              "Lifetime")

    def dropDownAdder():
        global ddPosY

        medTypeMenu.place(x=ddPosX, y=ddPosY)

        def change_dd(*args):
            tkvar2.set("Pick medicine..")
            tkvar3.set("Pick dosage..")
            tkvar4.set("Pick course duration..")
            global medType
            global medicine_list

            medType = tkvar1.get()[2:-3]
            curM.execute("SELECT trade_name from medicine where type = ?", (medType,))

            medicine_list.clear()
            for row in curM.fetchall():
                medicine_list.append(row)

            medNameMenu = OptionMenu(left, tkvar2, *medicine_list)
            medNameMenu.place(x=ddPosX + 140, y=ddPosY)

            def change_dd2(*args):
                global medName
                medName = tkvar2.get()[2:-3]

            tkvar2.trace('w', change_dd2)

            dosageMenu.place(x=ddPosX + 300, y=ddPosY)
            durationMenu.place(x=ddPosX + 450, y=ddPosY)

            def change_dd3(*args):
                global dose
                dose = tkvar3.get()

            tkvar3.trace('w', change_dd3)

            def change_dd4(*args):
                global duration
                duration = tkvar4.get()

            tkvar4.trace('w', change_dd4)

        tkvar1.trace('w', change_dd)

        printButton = Button(left, text="Print", width=10, height=1, bg="orange", command=printer)
        printButton.place(x=520, y=500)

        addButton = Button(left, text="Add", width=10, height=1, bg="orange", command=adder)
        addButton.place(x=420, y=500)

    def change_dropdown(*args):

        for i in tree.get_children():
            tree.delete(i)

        getName = tkvar.get()[2:-3]

        # Get problem
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
    returnButton.place(x=920, y=10)


class initUI:
    def __init__(self, master):
        runfunc(master)
