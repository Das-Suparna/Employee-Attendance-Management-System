from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import pyttsx3
from tkinter import ttk
from PIL import Image,ImageTk

global engine
engine  = pyttsx3.init()

selected_item = None
table = None
entry_boxes = {}

# Function to handle tree selection event
def on_tree_select(event):
    global selected_item, entry_boxes
    selected_item = table.focus()
    if selected_item:
        data = table.item(selected_item, "values")
        for i, col in enumerate(("Date", "Employee Id", "First Name","Last Name","Status", "Sign In", "Sign Out")):
            entry_boxes[col].delete(0, END)
            entry_boxes[col].insert(0, data[i])


def clear_data():
    for i, col in enumerate(("Date", "Employee Id", "First Name","Last Name","Status", "Sign In", "Sign Out")) :
        entry_boxes[col].delete(0, END)


# Function to update data
def update_data():
    global selected_item, entry_boxes

    if not selected_item:
        messagebox.showwarning("Error", "No row selected. Please select a row to update.", parent=window)
        return

    try:
        db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
        cursor = db.cursor()

        updated_data = []
        for col in ("Date", "Employee Id", "First Name","Last Name","Status", "Sign In", "Sign Out"):
            updated_data.append(entry_boxes[col].get())

        update_query = "UPDATE attendance SET `adate`=%s,`fname`=%s, `lname`=%s, `status`=%s, `sign_in`=%s, `outgoing`=%s WHERE `e_id`=%s"
        cursor.execute(update_query, (updated_data[0], updated_data[2], updated_data[3], updated_data[4],updated_data[5],updated_data[6], updated_data[1]))

        db.commit()
        
        engine.say("Data updated successfully!")
        engine.runAndWait()

        messagebox.showinfo("Success", "Data updated successfully!" ,parent=window)
        refresh_table()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error updating data: {e}" ,parent=window)

# Function to delete data

def delete_data():
    global selected_item, table

    if not selected_item:

        engine.say("No row selected. Please select a row to delete.")
        engine.runAndWait()

        messagebox.showwarning("Error", "No row selected. Please select a row to delete." ,parent=window)
        
        return

    try:
        db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
        cursor = db.cursor()

        selected_data = table.item(selected_item, "values")
        
        employee_id = selected_data[1]  # Assuming employee ID is in the second column

        delete_query = "DELETE FROM attendance WHERE `e_id`=%s"
        cursor.execute(delete_query, (employee_id,))

        db.commit()
       
        engine.say("Data deleted successfully!")
        engine.runAndWait()
     
        messagebox.showinfo("Success", "Data deleted successfully!" ,parent=window)

        clear_data()
        refresh_table()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error deleting data: {e}" ,parent=window)


# Function to refresh table data
def refresh_table():
    global table

    try:
        db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
        cursor = db.cursor()

        sqlquery = "SELECT * FROM attendance;"
        cursor.execute(sqlquery)
        rows = cursor.fetchall()

        # Clear the existing data in the table
        for row in table.get_children():
            table.delete(row)

        # Insert the updated data into the table
        for row in rows:
            table.insert("", "end", values=row)

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error refreshing table data: {e}" ,parent=window)


def viewEmployee():
    global table, entry_boxes, window

    window=Toplevel()
    window.title('The RiseShine Company')
    window.geometry("1200x578+180+100")
    window.configure(bg="#ffffff")
    window.resizable(False, False)

    window.iconphoto(False, PhotoImage(file = 'icon.png'))

    greet = Label(window, font=('verdana', 30, 'bold'), bg="white", text="Employee Attendance Record", width=500)
    greet.place(x=250,y=2,width=705,height=90)

    #----------id-------------------

    entire_reg = Frame(window,bd=2,bg="white",relief=RIDGE)
    entire_reg.place(x=30,y=130,width=510,height=350)

    db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
    cursor = db.cursor()

    sqlquery = "SELECT * FROM attendance;"
    print(sqlquery)

    try:
        cursor.execute(sqlquery)
        rows = cursor.fetchall()

        column_widths = (100, 70, 100, 100, 70,90,90)

        table = ttk.Treeview(window, columns=("Date", "Employee Id", "First Name","Last Name","Status", "Sign In", "Sign Out"), show="headings")
        table.place(x=520,y=130,width=650,height=350)

        table.heading("Date", text="Date")
        table.heading("Employee Id", text="Employee Id")
        table.heading("First Name", text="First Name")
        table.heading("Last Name", text="Last Name")
        table.heading("Status", text="Status")
        table.heading("Sign In", text="Sign In")
        table.heading("Sign Out", text="Sign Out")
   
        table.tag_configure("mytag", font=("Verdana", 10, "bold"))

        for i, col in enumerate(("Date", "Employee Id","First Name","Last Name", "Status", "Sign In", "Sign Out")):
            table.column(col, width=column_widths[i])

        for row in rows:
            table.insert("", "end", values=row)

        table.bind("<<TreeviewSelect>>", on_tree_select)  # Bind the selection event to the callback function

    except:
        messagebox.showinfo("Error", "Cannot Fetch data.")

    # Create the second table with Entry boxes
    entry_table_frame = Frame(window,bg="white")
    entry_table_frame.place(x=60,y=150,width=400,height=300)

    entry_boxes = {}
    for i, col in enumerate(("Date", "Employee Id","First Name","Last Name", "Status", "Sign In", "Sign Out")):
        label = Label(entry_table_frame, text=col,bg="white", font = ('arial', 14, 'bold'))
        label.grid(row=i, column=0, sticky=W, padx=5, pady=2)

        entry_box = Entry(entry_table_frame,bg="white", font = ('arial', 14, 'bold'), width=350)
        entry_box.grid(row=i, column=10, padx=70, pady=2)
        entry_boxes[col] = entry_box 

    # Update Data button
    update_button = Button(window, text="Update Data", bg="red",fg="white",font = ('arial', 15, 'bold'),command=update_data)
    update_button.place(x=60,y=420)

    # Delete Data button
    delete_button = Button(window, text="Delete Data", bg="red",fg="white",font = ('arial', 15, 'bold'),command=delete_data)
    delete_button.place(x=205,y=420)

    refresh_button = Button(window, text="Refresh Data", bg="red",fg="white",font = ('arial', 15, 'bold'),command=refresh_table)
    refresh_button.place(x=340,y=420)
    
    pass