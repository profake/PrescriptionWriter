from tkinter import *
import tkinter.messagebox
import sqlite3
import helpers
import tkinter.ttk as ttk
import tkinter.font as tkFont
import datetime
import os
now = datetime.datetime.now()

#db stuff
conn = sqlite3.connect('patient.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS log(id INTEGER NOT NULL PRIMARY KEY, client_name TEXT NOT NULL, client_phone TEXT NOT NULL, date_of_birth TEXT NOT NULL, gender TEXT NOT NULL, problem TEXT NOT NULL, status TEXT NOT NULL, last_visit TEXT)")
boxHeaders = ['ID', 'Name', 'Phone', 'Date of Birth', 'Gender', 'Problem',' Status', 'Last Visit']
items_list = []

def listPopulator():
    items_list.clear()
    cur.execute("SELECT * FROM log")
    for row in cur.fetchall():
        items_list.append(row)

def runfunc(master):
        #Colors and font
        itemFont = "calibri 14 bold"
        bgLight = '#161616'
        bgDark = '#333333'

        #canvas test
        canvas = Canvas(master, width=1280, height=50, bg = "orange", highlightthickness=0)
        canvas.pack()

        #Left panel
        left = Frame(master, width = 807, height = 664, bg = bgLight)
        left.pack(side = LEFT)

        #Left updater panel
        leftUpdater = Frame(master, width = 807, height = 664, bg = bgLight)

        #Right panel
        right = Frame(master, width = 765, height = 664, bg = bgDark)
        right.place(x=520, y=77)
        #right.pack()
        # Title
        title = Label(text="☇Patient Database", font='Ubuntu 26 bold', bg="orange", fg='white')
        title.place(x=0, y=0)

        # Add to log
        heading = Label(left, text="Add to log", font='Ubuntu 20 bold', bg=bgLight, fg='white')
        heading.place(x=10, y=30)

        # Log
        headingR = Label(right, text="Log", font='Ubuntu 20 bold', bg="orange", fg=bgLight)
        headingR.place(x=30, y=0)

        id = Label(left, text="ID:", font=(itemFont), bg=bgLight, fg='white')
        id.place(x=15, y=100)
        id_entry = Entry(left, width=30)
        id_entry.place(x=250, y=105)

        name = Label(left, text="Patient Name:", font=(itemFont), bg=bgLight, fg='white')
        name.place(x=15, y=140)
        name_entry = Entry(left, width=30)
        name_entry.place(x=250, y=145)

        phone = Label(left, text="Patient Phone:", font=(itemFont), bg=bgLight, fg='white')
        phone.place(x=15, y=180)
        phone_entry = Entry(left, width=30)
        phone_entry.place(x=250, y=185)

        dateOfBirth = Label(left, text="Date of Birth:", font=(itemFont), bg=bgLight, fg='white')
        dateOfBirth.place(x=15, y=220)
        dateOfBirth_entry = Entry(left, width=30)
        dateOfBirth_entry.place(x=250, y=225)

        gender = Label(left, text="Gender:", font=(itemFont), bg=bgLight, fg='white')
        gender.place(x=15, y=260)
        gender_entry = Entry(left, width=30)
        gender_entry.place(x=250, y=265)

        problem = Label(left, text="Problem:", font=(itemFont), bg=bgLight, fg='white')
        problem.place(x=15, y=300)
        problem_entry = Entry(left, width=30)
        problem_entry.place(x=250, y=305)

        def updater_panel():
            #Remove left panel
            left.pack_forget()

            #Add leftupdater to screen
            leftUpdater.pack(side = LEFT)
            headingUpd = Label(leftUpdater, text="Update log", font='Ubuntu 20 bold', bg=bgLight, fg='white')
            headingUpd.place(x=10, y=30)

            id = Label(leftUpdater, text="Enter ID to update:", font=(itemFont), bg=bgLight, fg='white')
            id.place(x=15, y=100)
            id_entry = Entry(leftUpdater, width=30)
            id_entry.place(x=250, y=105)

            # search button func
            def search():
                idVal = id_entry.get().strip()
                def update():
                    idVal = id_entry.get().strip()
                    nameVal = name_entry.get().strip()
                    phoneVal = Uphone_entry.get().strip()
                    dateOfBirthVal = UdateOfBirth_entry.get().strip()
                    genderVal = Ugender_entry.get().strip()
                    problemVal = Uproblem_entry.get().strip()
                    statusVal = Ustatus_entry.get().strip()
                    lastVisitVal = UlastVisit_entry.get().strip()
                    if idVal == '' or nameVal == '' or phoneVal == '' or dateOfBirthVal == '' or genderVal == '' or problemVal == '' or statusVal == '' or lastVisitVal == '':
                        tkinter.messagebox.showerror("Warning", "Please fill up all the entries")
                    else:
                        if not helpers.RepresentsInt(idVal):
                            tkinter.messagebox.showerror("Warning", "Please enter an integer value as ID")
                        else:
                            try:
                                cur.execute("UPDATE log SET id = ?, client_name = ?, client_phone = ?, date_of_birth = ?, gender = ?, problem = ?, status = ?, last_visit = ? WHERE id = ?",
                                            (idVal, nameVal, phoneVal, dateOfBirthVal, genderVal, problemVal, statusVal, lastVisitVal, idVal))
                                conn.commit()
                                dbtobox()
                                tkinter.messagebox.showinfo("Message",
                                                            "Entry updated successfully for ID: " + idVal + " " + nameVal)
                            except sqlite3.IntegrityError as e:
                                tkinter.messagebox.showerror("Error", "ID already in use")
                def delete():
                    delVal = int(idVal)
                    result = tkinter.messagebox.askquestion("Confirmation", "Are you sure you want to delete entry with ID: %d?" %delVal)
                    if result == 'yes':
                        cur.execute("DELETE FROM log WHERE id = ?", (delVal,))
                        conn.commit()
                        dbtobox()
                        tkinter.messagebox.showinfo("Information", "Entry %d was deleted sucessfully." %delVal)

                if idVal == "":
                    tkinter.messagebox.showerror("Error", "Please enter an ID")
                elif not helpers.RepresentsInt(idVal):
                    tkinter.messagebox.showerror("Error", "Please enter a valid integer ID")
                else:
                    idVal = int(idVal)
                    cur.execute("SELECT * FROM log WHERE id = ?", (idVal,))
                    data = cur.fetchall()
                    #if not means empty
                    if not data:
                        tkinter.messagebox.showerror("Error", "No such ID found")
                    else:

                        name = Label(leftUpdater, text="Client Name:", font=(itemFont), bg=bgLight, fg='white')
                        name.place(x=15, y=140)
                        name_entry = Entry(leftUpdater, width=30)
                        name_entry.place(x=250, y=145)
                        name_entry.insert(0, data[0][1])

                        Uphone = Label(leftUpdater, text="Client Phone:", font=(itemFont), bg=bgLight, fg='white')
                        Uphone.place(x=15, y=180)
                        Uphone_entry = Entry(leftUpdater, width=30)
                        Uphone_entry.place(x=250, y=185)
                        Uphone_entry.insert(0, data[0][2])

                        UdateOfBirth = Label(leftUpdater, text="Date of Birth:", font=(itemFont), bg=bgLight, fg='white')
                        UdateOfBirth.place(x=15, y=220)
                        UdateOfBirth_entry = Entry(leftUpdater, width=30)
                        UdateOfBirth_entry.place(x=250, y=225)
                        UdateOfBirth_entry.insert(0, data[0][3])

                        Ugender = Label(leftUpdater, text="Gender:", font=(itemFont), bg=bgLight, fg='white')
                        Ugender.place(x=15, y=260)
                        Ugender_entry = Entry(leftUpdater, width=30)
                        Ugender_entry.place(x=250, y=265)
                        Ugender_entry.insert(0, data[0][4])

                        Uproblem = Label(leftUpdater, text="Problem:", font=(itemFont), bg=bgLight, fg='white')
                        Uproblem.place(x=15, y=300)
                        Uproblem_entry = Entry(leftUpdater, width=30)
                        Uproblem_entry.place(x=250, y=305)
                        Uproblem_entry.insert(0, data[0][5])

                        Ustatus = Label(leftUpdater, text = "Status:", font=(itemFont), bg=bgLight, fg = 'white')
                        Ustatus.place(x = 15, y = 340)
                        Ustatus_entry = Entry(leftUpdater, width=30)
                        Ustatus_entry.place(x=250, y=345)
                        Ustatus_entry.insert(0, data[0][6])

                        UlastVisit = Label(leftUpdater, text = "Last visit:", font=(itemFont), bg=bgLight, fg='white')
                        UlastVisit.place(x = 15, y = 380)
                        UlastVisit_entry = Entry(leftUpdater, width=30)
                        UlastVisit_entry.place(x=250, y=385)
                        UlastVisit_entry.insert(0, data[0][7])

                        updateButton = Button(leftUpdater, text="Update Entry", width=10, height=1, bg="orange", command=update)
                        deleteButton = Button(leftUpdater, text="Delete Entry", width=10, height=1, bg="orange", command=delete)
                        updateButton.place(x=250, y=460)
                        deleteButton.place(x=350, y=460)
            #Back to entry panel
            def goback():
                leftUpdater.pack_forget()
                left.pack(side=LEFT)

            backButton = Button(leftUpdater, text="Go back", width=10, height=1, bg="orange", command=goback)
            backButton.place(x=415, y=40)
            searchButton = Button(leftUpdater, text = "Search", width = 5, height = 1, bg = "orange", command = search)
            searchButton.place(x=450, y=102)

        #--------------------------
        container = ttk.Frame(right)
        container.place(x=15, y=70)
        tree = ttk.Treeview(columns=boxHeaders, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
                            command=tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
                            command=tree.xview)
        tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        # --------------------------
        for col in boxHeaders:
                tree.heading(col, text=col,
                                  command=lambda c=col: sortby(tree, c, 0))
                # adjust the column's width to the header string
                tree.column(col,
                                 width=tkFont.Font().measure(col.title()))
        def dbtobox():
            listPopulator()

            # clear tree
            for i in tree.get_children():
                tree.delete(i)

            for item in items_list:
                tree.insert('', 'end', values=item)
                # adjust column's width if necessary to fit each value
                for ix, val in enumerate(item):
                    col_w = tkFont.Font().measure(val)
                    if tree.column(boxHeaders[ix], width=None) < col_w:
                        tree.column(boxHeaders[ix], width=col_w)
        dbtobox()

        #Scrolling box
        #box = Listbox(right, width=70, height=35)
        #box.place(x=15, y=70)

        def sortby(tree, col, descending):
            data = [(tree.set(child, col), child) \
                    for child in tree.get_children('')]
            data.sort(reverse=descending)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)
            tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

        def clearentries():
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            phone_entry.delete(0, END)
            dateOfBirth_entry.delete(0, END)
            gender_entry.delete(0, END)
            problem_entry.delete(0, END)

        def submit():
            idVal = id_entry.get().strip()
            nameVal = name_entry.get().strip()
            phoneVal = phone_entry.get().strip()
            dateOfBirthVal = dateOfBirth_entry.get().strip()
            genderVal = gender_entry.get().strip()
            problemVal = problem_entry.get().strip()

            if idVal == '' or nameVal == '' or phoneVal == '' or dateOfBirthVal == '' or genderVal == '' or problemVal == '':
                tkinter.messagebox.showerror("Warning", "Please fill up all the entries")
            else:
                if not helpers.RepresentsInt(idVal):
                    tkinter.messagebox.showerror("Warning", "Please enter an integer value as ID")
                else:
                    try:
                        currentDate = str(now.day)+'-'+str(now.month)+'-'+str(now.year)
                        cur.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (idVal, nameVal, phoneVal, dateOfBirthVal, genderVal, problemVal, 'Not Done', currentDate))
                        conn.commit()
                        dbtobox()
                        tkinter.messagebox.showinfo("Message", "Entry added successfully for " + nameVal + " ")
                        clearentries()
                    except sqlite3.IntegrityError as e:
                        tkinter.messagebox.showerror("Error", "ID already in use")
        def returnToPicker():
            master.destroy()
            os.system('python windowPickerStarter.py')

        returnButton = Button(canvas, text="Return", width=10, height=1, bg="white", command=returnToPicker)
        returnButton.place(x=800, y=20)

        submitButton = Button(left, text = "Add Entry", width = 10, height = 1, bg = "orange", command = submit)
        clearButton = Button(left, text = "Clear", width = 5, height = 1, bg = "orange", command = clearentries)
        updateButton = Button(left, text="Update", width = 10, height= 2, bg = "orange", command = updater_panel)
        submitButton.place (x=315, y=400)
        clearButton.place (x=265, y=400)
        updateButton.place(x=290, y=450)

class presc:
    def __init__(self, master):
        runfunc(master)
