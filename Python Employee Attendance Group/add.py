from tkinter import *
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import pyttsx3  
from datetime import datetime
from tkcalendar import Calendar

global engine
engine = pyttsx3.init() 

def add_db():

    global id
    global lname
    global fname
    global eadd
    global econtact
    global e_email
    global ejoin
    global egender
    global edob
    global edept

    e_id = id.get()									
    efname = fname.get()
    elname = lname.get()
    eadd2 = eadd.get()
    econtact2 = econtact.get()
    e_email2 = e_email.get()
    ejoin2 = ejoin.get()
    egender2 = egender.get()
    edob2 = edob.get()
    edept2 = edept.get()
   
    engine = pyttsx3.init()  
    
    db = mysql.connector.connect(host ="localhost",user = "root",password = '',database='employee_attendance_db')
    cursor = db.cursor()
    
    print(e_id,end='--')									
    print(efname,end='--')
    print(elname,end='--')
    print(eadd2,end='--')
    print(econtact2,end='--')
    print(e_email2,end='--')
    print(ejoin2,end='--')
    print(egender2,end='--')
    print(edob2,end='--')
    print(edept2,end='--')
  
    print("Register")

    sqlquery= "insert into employee values('" + e_id +"','"+efname+"','"+elname+"','"+eadd2+"','"+econtact2+"','"+e_email2+"','"+ejoin2+"','"+egender2+"','"+edob2+"','"+edept2+"');"
    print(sqlquery)

    try:
        cursor.execute(sqlquery)
        
        engine.say("Employee Registered Successfully" )  
        engine.runAndWait() 

        db.commit()
        messagebox.showinfo('Success',"Employee Registered Successfully" ,parent=window)
    except:  
        engine.say("Cannot add Employee into Database" )  
        engine.runAndWait()
        messagebox.showinfo("Error","Cannot add Employee into Database" ,parent=window)
        

    # Global variables

global selected_item
global tree
global entry_boxes
selected_item = None
tree = None
entry_boxes = {}

    # Function to handle tree selection event
def on_tree_select(event):
    global selected_item, entry_boxes
    selected_item = tree.focus()
    if selected_item:
        data = tree.item(selected_item, "values")

        id.delete(0, END)
        id.insert(0, data[0])

        lname.delete(0, END)
        lname.insert(0, data[2])
        
        fname.delete(0, END)
        fname.insert(0, data[1])
        
        eadd.delete(0, END)
        eadd.insert(0, data[3])
        
        econtact.delete(0, END)
        econtact.insert(0, data[4])
        
        e_email.delete(0, END)
        e_email.insert(0, data[5])
        
        ejoin.delete(0, END)
        ejoin.insert(0, data[6])
        
        egender.delete(0, END)
        egender.insert(0, data[7])
        
        edob.delete(0, END)
        edob.insert(0, data[8])
        
        edept.delete(0, END)
        edept.insert(0, data[9])

    # Function to update data
def update_data():
    global selected_item
    global id, lname, fname, eadd, econtact, e_email , ejoin, egender, edob, edept

    if not selected_item:
        messagebox.showwarning("Error", "No row selected. Please select a row to update." ,parent=window)
        return

    try:
        db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
        cursor = db.cursor()

        updated_data = []
        
        updated_data.append(id.get())
        updated_data.append(fname.get())
        updated_data.append(lname.get())   
        updated_data.append(eadd.get())       
        updated_data.append(econtact.get())      
        updated_data.append(e_email.get())    
        updated_data.append(ejoin.get())   
        updated_data.append(egender.get())
        updated_data.append(edob.get())
        updated_data.append(edept.get())


        update_query = "UPDATE employee SET `efname`=%s, `elname`=%s, `eadd`=%s, `econtact`=%s, `e_email`=%s, `ejoin`=%s, `egender`=%s, `edob`=%s, `edept`=%s WHERE `e_id`=%s"
        cursor.execute(update_query, tuple(updated_data[1:] + [updated_data[0]]))  # Use selected_item as the Employee ID

        db.commit()

        engine.say("Data updated successfully")
        engine.runAndWait()


        messagebox.showinfo("Success", "Data updated successfully" ,parent=window)
        refresh_table()  # Update the table after the data is updated


    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error updating data: {e}" ,parent=window)


    # Function to delete data
def delete_data():
    global selected_item
    data = tree.item(selected_item, "values")

    if not selected_item:
        messagebox.showwarning("Error", "No row selected. Please select a row to delete." ,parent=window)
        return

    try:
        db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
        cursor = db.cursor()

        eid= data[0]
        delete_query = "DELETE FROM employee WHERE `e_id`=%s"
        cursor.execute(delete_query, (eid,))

        delete_attend = "DELETE FROM attendance WHERE `e_id`=%s"
        cursor.execute(delete_attend, (eid,))

        db.commit() 

        engine.say("Data deleted successfully!")
        engine.runAndWait()

        messagebox.showinfo("Success", "Data deleted successfully!" ,parent=window)
        
        refresh_table()  # Update the table after the data is deleted
        clear_data()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error deleting data: {e}" ,parent=window)


    # Function to refresh table data
def refresh_table():
    global tree

    try:
        db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
        cursor = db.cursor()

        sqlquery = "SELECT * FROM employee;"
        cursor.execute(sqlquery)
        rows = cursor.fetchall()

        # Clear the existing data in the tree
        for row in tree.get_children():
            tree.delete(row)

            # Insert the updated data into the tree
        for row in rows:
            tree.insert("", "end", values=row)

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error refreshing table data: {e}" ,parent=window)




def display_attendance():

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee_attendance_db"
        )

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employee")
        results = cursor.fetchall()

        # Clear existing data from the Treeview
        tree.delete(*tree.get_children())

        
        for row in results:
            tree.insert("", tk.END, values=row)
 
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}" ,parent=window)



def clear_data():

        id.delete(0, END)        
        lname.delete(0, END)
        fname.delete(0, END)
        eadd.delete(0, END)
        econtact.delete(0, END)     
        ejoin.delete(0, END)
        egender.delete(0, END)      
        edob.delete(0, END)
        edept.delete(0, END)
        e_email.delete(0, END)


month_dict = {"January": "01","February": "02","March": "03","April": "04","May": "05","June": "06","July": "07","August": "08","September": "09","October": "10","November": "11","December": "12"}


def get_date_dob():
    day = int(day_combo.get())
    month = month_combo.get()
    year = int(year_combo.get())

    formatted_date = f"{year}-{month_dict[month]}-{day:02d}"
    a = text=f"{formatted_date}"
    edob.delete(0, "end")
    edob.insert(0,a)
    

    
def get_date():
    day = int(day_combobox.get())
    month = month_combobox.get()
    year = int(year_combobox.get())

    formatted_date = f"{year}-{month_dict[month]}-{day:02d}"
    a = text=f"{formatted_date}"
    ejoin.delete(0, "end")
    ejoin.insert(0,a)




def addEmp():

    global id, lname, fname, eadd, econtact
    global e_email 
    global ejoin
    global egender
    global edob
    global edept
    global listbox
    global tree
    global window
    global day_combobox
    global month_combobox
    global year_combobox
    global day_combo
    global month_combo
    global year_combo
    global ejoin

    window=Toplevel()
    window.title('The RiseShine Company')
    window.geometry("1300x758+100+20")
 
    window.configure(bg="#ffffff")
    window.resizable(False, False)
    
    window.iconphoto(False, PhotoImage(file="icon.png"))

    # Current Course 

    title_add = Frame(window,bd=2,bg="white",relief=RIDGE)
    title_lb1 = Label(window,text="EMPLOYEE REGISTRATION FORM",font=("Verdana",30,"bold"),fg="black",bg="white")
    title_lb1.place(x=80,y=4,width=1100,height=50)

    title_add.place(x=40,y=2,width=1200,height=60)

    entire_reg = Frame(window,bd=2,bg="white",relief=RIDGE)
    entire_reg.place(x=30,y=90,width=1205,height=400)


    #Student id
    L = Label(window,text="Enter Employee id:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=40, y=100,width=250, height=30)
    id = Entry(window,width=15,font=("Verdana",12,"bold"))
    id.place(x=300, y=100,width=250, height=30)

    L = Label(window,text="First Name:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=40, y=140,width=250, height=30)
    fname = Entry(window,width=15,font=("Verdana",12,"bold"))
    fname.place(x=300, y=140,width=250, height=30)

    L = Label(window,text="Last Name:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=40, y=180,width=250, height=30)
    lname = Entry(window,width=15,font=("Verdana",12,"bold"))
    lname.place(x=300, y=180,width=250, height=30)

    L = Label(window,text="Enter Address:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=40, y=220,width=250, height=30)
    eadd = Entry(window,width=15,font=("Verdana",12,"bold"))
    eadd.place(x=300, y=220,width=250, height=30)

    L = Label(window,text="Contact No:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=40, y=260,width=250, height=30)
    econtact = Entry(window,width=15,font=("Verdana",12,"bold"))
    econtact.place(x=300, y=260,width=250, height=30)

    L = Label(window,text="Email ID:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=40, y=300,width=250, height=30)
    e_email = Entry(window,width=15,font=("Verdana",12,"bold"))
    e_email.place(x=300, y=300,width=250, height=30)

    L = Label(window,text="Department:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=40, y=340,width=250, height=30)
    edept = Entry(window,width=15,font=("Verdana",12,"bold"))
    edept.place(x=300, y=340,width=250, height=30)

#radio buttons for gender

    selected_option = tk.StringVar()
    option1 = tk.Radiobutton(window, text="Male", variable=selected_option, value="Male", fg="black", bg="white", font=("Verdana", 10,"bold"))
    option2 = tk.Radiobutton(window, text="Female", variable=selected_option, value="Female", fg="black", bg="white", font=("Verdana", 10,"bold"))
    L = tk.Label(window, text="Gender:", font=("Verdana", 12, "bold"), fg="black", bg="white")
    L.place(x=625, y=200, width=250, height=30)

    egender = tk.Entry(window, textvariable=selected_option, width=15, font=("Verdana", 12, "bold"))
    egender.place(x=910, y=200, width=250, height=30)
        
    option1.place(x=910, y=240, width=60, height=30)
    option2.place(x=990, y=240, width=70, height=30)

#second half

    cur_date = datetime.now()

#dates dob
    L = Label(window,text="Date Of Birth:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=650, y=110,width=250, height=30)

    # Day Combo Box with default to current day
    day_combo = ttk.Combobox(window, values=list(range(1, 32)), font=("Verdana",10,"bold"))
    day_combo.set(cur_date.day)  # Set the default value to the current day
    day_combo.place(x=910, y=110,width=40, height=30)

    # Month Combo Box with default to current month
    month_combo = ttk.Combobox(window, values=list(month_dict.keys()),font=("Verdana",10,"bold"))
    month_combo.set(cur_date.strftime("%B"))  # Set the default value to the current month
    month_combo.place(x=960, y=110,width=110, height=30)

    # Year Combo Box with default to current year
    current_year = cur_date.year
    year_combo = ttk.Combobox(window, values=list(range(current_year - 50, current_year+1)), font=("Verdana",10,"bold"))
    year_combo.set(current_year)  # Set the default value to the current year
    year_combo.place(x=1080, y=110,width=60, height=30)

    # Button to Get the Date
    get_dob = tk.Button(window, text="Get DOB", command=get_date_dob, bg="blue",fg="white", font = ('Verdana', 10, 'bold'))
    get_dob.place(x=910, y=150,width=110, height=30)

    # Display Selected Date
    edob = Entry(window, text="",font=("Verdana",10,"bold"),fg="black",bg="white")
    edob.place(x=1030, y=150,width=110, height=30)
 
    #dates joining
    L = Label(window,text="Joining Date:",font=("Verdana",12,"bold"),fg="black",bg="white")
    L.place(x=640, y=300,width=250, height=30)

    # Day Combo Box with default to current day
    day_combobox = ttk.Combobox(window, values=list(range(1, 32)), font=("Verdana",10,"bold"))
    day_combobox.set(cur_date.day)  # Set the default value to the current day
    day_combobox.place(x=910, y=290,width=40, height=30)

    # Month Combo Box with default to current month
    month_combobox = ttk.Combobox(window, values=list(month_dict.keys()),font=("Verdana",10,"bold"))
    month_combobox.set(cur_date.strftime("%B"))  # Set the default value to the current month
    month_combobox.place(x=960, y=290,width=110, height=30)

    # Year Combo Box with default to current year
    current_year = cur_date.year
    year_combobox = ttk.Combobox(window, values=list(range(current_year - 50, current_year+1)), font=("Verdana",10,"bold"))
    year_combobox.set(current_year)  # Set the default value to the current year
    year_combobox.place(x=1080, y=290,width=60, height=30)

    # Button to Get the Date
    get_date_button = tk.Button(window, text="Get Join Date", command=get_date, bg="green",fg="white", font = ('Verdana', 10, 'bold'))
    get_date_button.place(x=910, y=330,width=110, height=30)

    # Display Selected Date
    ejoin = Entry(window, text="",font=("Verdana",10,"bold"),fg="black",bg="white")
    ejoin.place(x=1030, y=330,width=110, height=30)

    #Button Frame
    btn_frame = Frame(window,bd=2,bg="white",relief=RIDGE)
    btn_frame.place(x=320,y=400,width=665,height=60)

    submitbtn=Button(btn_frame,text="Register",command=add_db,bg="#ff413b",fg="white", font = ('arial', 15, 'bold'))
    submitbtn.grid(row=20, column=2,padx=5,pady=10,sticky=W)
        
    # Update Data button
    update_button = Button(btn_frame, text="Update Data", command=update_data,bg="#ff413b",fg="white", font = ('arial', 15, 'bold'))
    update_button.grid(row=20, column=3,padx=5,pady=10,sticky=W)

    # Delete Data button
    delete_button = Button(btn_frame, text="Delete Data", command=delete_data,bg="#ff413b",fg="white", font = ('arial', 15, 'bold'))
    delete_button.grid(row=20, column=4,padx=5,pady=10,sticky=W)

    #display button  
    display_button = Button(btn_frame, text="Display Data", command=display_attendance,bg="#ff413b",fg="white", font = ('arial', 15, 'bold'))
    display_button.grid(row=20, column=5,padx=5,pady=10,sticky=W)

    #clear button
    clear_button= Button(btn_frame, text="Clear Data", command=clear_data,bg="#ff413b",fg="white", font = ('arial', 15, 'bold'))
    clear_button.grid(row=20, column=6,padx=5,pady=10,sticky=W)


    tree = ttk.Treeview(window, columns=("Employee ID", "First Name", "Last Name", "Address", "Contact No.", "Email", "Join Date", "Gender", "Date Of Birth", "Department"), show="headings")
    tree.heading("Employee ID", text="Employee ID")
    tree.heading("Last Name", text="Last Name")
    tree.heading("First Name", text="First Name")
    tree.heading("Address", text="Address")
    tree.heading("Contact No.", text="Contact No.")
    tree.heading("Email", text="Email")
    tree.heading("Join Date", text="Join Date")
    tree.heading("Gender", text="Gender")
    tree.heading("Date Of Birth", text="Date Of Birth")
    tree.heading("Department", text="Department")

    tree.bind("<ButtonRelease-1>", on_tree_select)
    # Create vertical scrollbars
    yscrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)

    tree.grid(row=0, column=0, sticky="nsew")

    yscrollbar.place(x=1225,y=500, height=200)

    for col in tree["columns"]:
        tree.column(col, width=120, stretch=tk.NO)

    # Configure row height
    tree.configure(yscrollcommand=yscrollbar.set, height=10)
    tree.place(x=30,y=500, height=200) 

    pass