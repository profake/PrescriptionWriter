from tkinter import *
import tkinter.messagebox
import sqlite3
import helpers
import tkinter.ttk as ttk
import tkinter.font as tkFont
import os

# db stuff
conn = sqlite3.connect('medicine_database.db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS medicine(type TEXT NOT NULL, trade_name TEXT NOT NULL PRIMARY KEY, company TEXT NOT NULL, power INTEGER NOT NULL)")
boxHeaders = ['Type', 'Trade Name', 'Company', 'Power']
items_list = []

def listPopulator():
    items_list.clear()
    cur.execute("SELECT * FROM medicine")
    for row in cur.fetchall():
        items_list.append(row)

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

        #Left updater panel
        leftUpdater = Frame(master, width = 807, height = 664, bg = bgLight)

        #Right panel
        right = Frame(master, width = 765, height = 664, bg = bgDark)
        right.place(x=520, y=77)
        #right.pack()
        # Title
        title = Label(text="☇Medicine Database", font='Ubuntu 26 bold', bg="orange", fg='white')
        title.place(x=0, y=0)

        # Add to log
        heading = Label(left, text="Add to medicine", font='Ubuntu 20 bold', bg=bgLight, fg='white')
        heading.place(x=10, y=30)

        # Log
        headingR = Label(right, text="Medicine", font='Ubuntu 20 bold', bg="orange", fg=bgLight)
        headingR.place(x=30, y=0)

        type = Label(left, text="Type:", font=(itemFont), bg=bgLight, fg='white')
        type.place(x=15, y=100)
        type_entry = Entry(left, width=30)
        type_entry.place(x=250, y=105)

        name = Label(left, text="Trade Name:", font=(itemFont), bg=bgLight, fg='white')
        name.place(x=15, y=140)
        name_entry = Entry(left, width=30)
        name_entry.place(x=250, y=145)

        company = Label(left, text="Company:", font=(itemFont), bg=bgLight, fg='white')
        company.place(x=15, y=180)
        company_entry = Entry(left, width=30)
        company_entry.place(x=250, y=185)

        power = Label(left, text="Power", font=(itemFont), bg=bgLight, fg='white')
        power.place(x=15, y=220)
        power_entry = Entry(left, width=30)
        power_entry.place(x=250, y=225)

        def deleter_panel():
            #Remove left panel
            left.pack_forget()

            #Add leftupdater to screen
            leftUpdater.pack(side = LEFT)
            headingUpd = Label(leftUpdater, text="Delete", font='Ubuntu 20 bold', bg=bgLight, fg='white')
            headingUpd.place(x=10, y=30)

            findName = Label(leftUpdater, text="Enter trade name to delete:", font=(itemFont), bg=bgLight, fg='white')
            findName.place(x=15, y=100)
            findName_entry = Entry(leftUpdater, width=30)
            findName_entry.place(x=250, y=105)

            def delete():
                findNameVal = findName_entry.get().strip()
                if(findNameVal == ""):
                    tkinter.messagebox.showerror("Warning", "Please enter a name")
                else:
                    cur.execute("SELECT * FROM medicine WHERE trade_name = ?", (findNameVal,))
                    data = cur.fetchall()
                    if not data:
                        tkinter.messagebox.showerror("Error", "No such trade name found")
                    else:
                        result = tkinter.messagebox.askquestion("Confirmation", "Are you sure you want to delete ?")
                        if result == 'yes':
                            cur.execute("DELETE FROM medicine WHERE trade_name = ?", (findNameVal,))
                            conn.commit()
                            dbtobox()
                            tkinter.messagebox.showinfo("Information", "Entry was deleted sucessfully.")

            #Back to entry panel
            def goback():
                leftUpdater.pack_forget()
                left.pack(side=LEFT)

            backButton = Button(leftUpdater, text="Go back", width=10, height=1, bg="orange", command=goback)
            backButton.place(x=415, y=40)
            searchButton = Button(leftUpdater, text = "Search", width = 5, height = 1, bg = "orange", command = delete)
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
            type_entry.delete(0, END)
            name_entry.delete(0, END)
            company_entry.delete(0, END)
            power_entry.delete(0, END)

        def submit():
            typeVal = type_entry.get().strip()
            nameVal = name_entry.get().strip()
            companyVal = company_entry.get().strip()
            powerVal = power_entry.get().strip()

            if typeVal == '' or nameVal == '' or companyVal == '' or powerVal == '':
                tkinter.messagebox.showerror("Warning", "Please fill up all the entries")
            else:
                if not helpers.RepresentsInt(powerVal):
                    tkinter.messagebox.showerror("Warning", "Please enter an integer value as power")
                else:
                    try:
                        cur.execute("INSERT INTO medicine VALUES(?, ?, ?, ?)",
                                (typeVal, nameVal, companyVal, powerVal+" mg"))
                        conn.commit()
                        dbtobox()
                        tkinter.messagebox.showinfo("Message", "Entry added successfully for " + nameVal + " of brand " + companyVal + " with power "+powerVal)
                        clearentries()
                    except sqlite3.IntegrityError as e:
                        tkinter.messagebox.showerror("Error", "ERROR!")

        def returnToPicker():
            master.destroy()
            os.system('python windowPickerStarter.py')

        returnButton = Button(canvas, text="Return", width=10, height=1, bg="white", command=returnToPicker)
        returnButton.place(x=800, y=20)

        submitButton = Button(left, text = "Add Entry", width = 10, height = 1, bg = "orange", command = submit)
        clearButton = Button(left, text = "Clear", width = 5, height = 1, bg = "orange", command = clearentries)
        submitButton.place (x=315, y=400)
        clearButton.place (x=265, y=400)
        deleteButton = Button(left, text="Delete", width = 10, height= 2, bg = "orange", command = deleter_panel)
        deleteButton.place(x=290, y=450)

class initUI:
    def __init__(self, master):
        runfunc(master)
