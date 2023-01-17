# Import modules
from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas

# Function to exit the GUI database management system
def exit():
    result=messagebox.askyesno('Confirm','Exit the program?') # Requires confirmation 
    if result:
        window.destroy()
    else:
        pass

# Function to export the swimmer profile
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=swimTable.get_children()
    newlist=[]
    for index in indexing:
        content=swimTable.item(index)
        datalist=content['values']
        newlist.append(datalist)


    table=pandas.DataFrame(newlist,columns=['Id','Name','Age','Club','Hometown','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is exported succesfully')


def toplevel_data(title,button_text,command):
    global idEntry,ageEntry,nameEntry,clubEntry,hometownEntry,genderEntry,dobEntry,addWindow
    addWindow = Toplevel()
    addWindow.title(title)
    addWindow.grab_set()
    addWindow.resizable(False, False)
    idLabel = Label(addWindow, text='Id', font=('arial', 20))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(addWindow, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(addWindow, text='Name', font=('arial', 20))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(addWindow, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    ageLabel = Label(addWindow, text='Age', font=('arial', 20))
    ageLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    ageEntry = Entry(addWindow, font=('arial', 20), width=24)
    ageEntry.grid(row=2, column=1, pady=15, padx=10)

    clubLabel = Label(addWindow, text='Club', font=('arial', 20))
    clubLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    clubEntry = Entry(addWindow, font=('arial', 20), width=24)
    clubEntry.grid(row=3, column=1, pady=15, padx=10)

    hometownEntry = Label(addWindow, text='Hometown', font=('arial', 20))
    hometownEntry.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    hometownEntry = Entry(addWindow, font=('arial', 20), width=24)
    hometownEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(addWindow, text='Gender', font=('arial', 20))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(addWindow, font=('arial', 20), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(addWindow, text='D.O.B', font=('arial', 20))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(addWindow, font=('arial', 20), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    swimmerBtn = ttk.Button(addWindow, text=button_text, command=command)
    swimmerBtn.grid(row=7, columnspan=2, pady=15)

    if title=='Update Swimmer Profile':
        indexing = swimTable.focus()

        content = swimTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        ageEntry.insert(0, listdata[2])
        clubEntry.insert(0, listdata[3])
        hometownEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

# Update a swimmer profile
def update_swimmer():
    query='update swimmer set name=%s,age=%s,club=%s,hometown=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycur.execute(query,(nameEntry.get(),ageEntry.get(),clubEntry.get(),hometownEntry.get(),
                            genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} has been updated',parent=addWindow)
    addWindow.destroy()
    show_swimmer()


# Show a swimmer
def show_swimmer():
    query = 'select * from swimmer'
    mycur.execute(query)
    fetched_data = mycur.fetchall()
    swimTable.delete(*swimTable.get_children())
    for data in fetched_data:
        swimTable.insert('', END, values=data)

# Delete a swimmer profile
def del_swimmer():
    indexing=swimTable.focus()
    print(indexing)
    content=swimTable.item(indexing)
    content_id=content['values'][0]
    query='delete from swimmer where id=%s'
    mycur.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} has been deleted')
    query='select * from swimmer'
    mycur.execute(query)
    fetched_data=mycur.fetchall()
    swimTable.delete(*swimTable.get_children())
    for data in fetched_data:
        swimTable.insert('',END,values=data)

# Find a swimmer
def search_swimmer():
    query='select * from swimmer where id=%s or name=%s or club=%s or age=%s or hometown=%s or gender=%s or dob=%s'
    mycur.execute(query,(idEntry.get(),nameEntry.get(),clubEntry.get(),ageEntry.get(),hometownEntry.get(),genderEntry.get(),dobEntry.get()))
    swimTable.delete(*swimTable.get_children())
    fetched_data=mycur.fetchall()
    for data in fetched_data:
        swimTable.insert('',END,values=data)

# Add a swimmer to the database
def add_swimmer():
    if idEntry.get()=='' or nameEntry.get()=='' or ageEntry.get()=='' or clubEntry.get()=='' or hometownEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('Error','Please enter information to all fields.',parent=addWindow)

    else:
        try:
            query='insert into swimmer values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycur.execute(query,(idEntry.get(),nameEntry.get(),ageEntry.get(),clubEntry.get(),hometownEntry.get(),
                                    genderEntry.get(),dobEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=addWindow)
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0,END)
                ageEntry.delete(0,END)
                clubEntry.delete(0,END)
                hometownEntry.delete(0,END)
                genderEntry.delete(0,END)
                dobEntry.delete(0,END)
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=addWindow)
            return


        query='select *from swimmer'
        mycur.execute(query)
        fetched_data=mycur.fetchall()
        swimTable.delete(*swimTable.get_children())
        for data in fetched_data:
            swimTable.insert('',END,values=data)

# Connect to local database
def connect_database():
    def connect():
        global mycur,con
        try:
            con=pymysql.connect(host='localhost',user='root',password='i?901roUT3!')
            mycur=con.cursor()
        except:
            messagebox.showerror('Error','Invalid information',parent=connectWindow)
            return

        try:
            query='create database swimmer_data'
            mycur.execute(query)
            query='use swimmer_data'
            mycur.execute(query)
            query='create table swimmer(id int not null primary key, name varchar(30),age varchar(3),club varchar(10),' \
                  'hometown varchar(50),gender varchar(1),dob varchar(20),date varchar(50), time varchar(50))'
            mycur.execute(query)
        except:
            query='use studentmanagementsystem'
            mycur.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
        connectWindow.destroy()
        addswimmerBtn.config(state=NORMAL)
        findswimmerBtn.config(state=NORMAL)
        updateswimmerBtn.config(state=NORMAL)
        showswimmerBtn.config(state=NORMAL)
        exportswimmerBtn.config(state=NORMAL)
        delswimmerBtn.config(state=NORMAL)


    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)

# Display current time
def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    dateLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    dateLabel.after(1000,clock)


window = ttkthemes.ThemedTk()

window.get_themes()
window.set_theme("aquativo")

window.geometry("1000x700+50+20") 
window.title("Swimmer Profile")
window.resizable(False, False) 

dateLabel = Label(window, text="Today", font=("arial", 14))
dateLabel.place(x=5, y=5)
clock()


s = "Swimmer Profile Management System"
dtbnameLabel = Label(window, text=s, font=("arial", 20, "bold"))
dtbnameLabel.place(x = 230, y = 0)

dtbButton = ttk.Button(window, text='Connect database', command=connect_database)
dtbButton.place(x=800, y=0)

leftFrame = Frame(window)
leftFrame.place(x=50, y=80, width=300, height=550)

addswimmerBtn = ttk.Button(leftFrame, text="Add swimmer", width=25, state=DISABLED, command=add_swimmer)
addswimmerBtn.grid(row=1, column=0, pady = 20)

findswimmerBtn = ttk.Button(leftFrame, text="Find swimmer", width=25, state=DISABLED, command=search_swimmer)
findswimmerBtn.grid(row=2, column=0, pady = 20)

delswimmerBtn = ttk.Button(leftFrame, text="Delete swimmer", width=25, state=DISABLED, command=del_swimmer)
delswimmerBtn.grid(row=3, column=0, pady = 20)

updateswimmerBtn = ttk.Button(leftFrame, text="Update swimmer", width=25, state=DISABLED, command=update_swimmer)
updateswimmerBtn.grid(row=4, column=0, pady = 20)

showswimmerBtn = ttk.Button(leftFrame, text="Show swimmer", width=25, state=DISABLED, command=show_swimmer)
showswimmerBtn.grid(row=5, column=0, pady = 20)

exportswimmerBtn = ttk.Button(leftFrame, text="Export swimmer data", width=25, state=DISABLED)
exportswimmerBtn.grid(row=5, column=0, pady = 20)

exitBtn = ttk.Button(leftFrame, text="Exit", width=25, state=DISABLED)
exitBtn.grid(row=6, column=0, pady = 20)

rightFrame = Frame(window)
rightFrame.place(x=300, y=80, width=650, height=550)

horscrollBar = ttk.Scrollbar(rightFrame, orient=HORIZONTAL)
verscrollBar = ttk.Scrollbar(rightFrame, orient=VERTICAL)

swimTable=ttk.Treeview(rightFrame,columns=('Id','Name','Age','Club','Hometown','Gender',
                                 'D.O.B','Added Date','Added Time'),
                          xscrollcommand=horscrollBar.set,yscrollcommand=verscrollBar.set)

horscrollBar.config(command=swimTable.xview)
verscrollBar.config(command=swimTable.yview)

horscrollBar.pack(side=BOTTOM,fill=X)
verscrollBar.pack(side=RIGHT,fill=Y)

swimTable.pack(expand=1,fill=BOTH)

swimTable.heading('Id',text='Id')
swimTable.heading('Name',text='Name')
swimTable.heading('Age',text='Age')
swimTable.heading('Club',text='Swim Club')
swimTable.heading('Hometown',text='Hometown')
swimTable.heading('Gender',text='Gender')
swimTable.heading('D.O.B',text='D.O.B')
swimTable.heading('Added Date',text='Added Date')
swimTable.heading('Added Time',text='Added Time')

swimTable.column('Id',width=50,anchor=CENTER)
swimTable.column('Name',width=200,anchor=CENTER)
swimTable.column('Club',width=300,anchor=CENTER)
swimTable.column('Age',width=200,anchor=CENTER)
swimTable.column('Hometown',width=300,anchor=CENTER)
swimTable.column('Gender',width=100,anchor=CENTER)
swimTable.column('D.O.B',width=200,anchor=CENTER)
swimTable.column('Added Date',width=200,anchor=CENTER)
swimTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40,font=('arial', 12), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14),foreground='cyan4')

swimTable.config(show='headings')

window.mainloop()