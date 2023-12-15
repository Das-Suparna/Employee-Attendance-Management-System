from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import pyttsx3  
from  datetime import *
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image,ImageTk

global engine
engine  = pyttsx3.init()

def add_db2():
    global id
    global outgoing, efname, elname

    initial_date = datetime.now().strftime('%Y-%m-%d')
    initial_time = datetime.now().strftime('%H:%M:%S')
    a_id = id.get()
    a_date = initial_date
    a_status = "Present"
    a_signin = initial_time
    a_outgoing = "00:00:00"


    db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
    cursor = db.cursor()

    print(a_id, end='--')
    print(a_date, end='--')
    print(a_status, end='--')
    print(a_signin, end='--')
    print(a_outgoing, end='--')
    print("Attendance")

    sqlquery = "insert into attendance(`adate`,`e_id`,`fname`,`lname`,`status`,`sign_in`,`outgoing`) values('" + a_date + "','" + a_id + "','" + efname + "','" + elname + "','" + a_status + "','" + a_signin + "','" + a_outgoing + "');"
    print(sqlquery)

    try:
        cursor.execute(sqlquery)
        db.commit()
        messagebox.showinfo('Success', "Attendance Registered Successfully" ,parent=window)
    except mysql.connector.Error as err:
        
        db.rollback()
        messagebox.showerror("Error", f"Error: {err}" ,parent=window)


def sign_in():
    employee_id = id.get()
    sign_out_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        conn = mysql.connector.connect(host="localhost",user="root",password="",database="employee_attendance_db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM attendance WHERE adate=%s AND e_id=%s and sign_in is not null", (current_date, employee_id))
        result = cursor.fetchone()

        cursor.close()  # Close the cursor after fetching the result

        if not result:
            # Employee hasn't signed in today, so insert a new entry

            engine.say("Employee has successfully signed in.")
            engine.runAndWait()
            add_db2()          
            conn.commit()
        else:
            
            engine.say("Employee has already signed in for today.")
            engine.runAndWait()
            messagebox.showinfo("Sign-In Error", "Employee has already signed in for today." ,parent=window)

        conn.close()
    except Exception as e:
        
        messagebox.showinfo("Sign-In Error", "Employee has already signed in for today." ,parent=window)


def sign_out():
    employee_id = id.get()
    sign_out_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        conn = mysql.connector.connect(host="localhost",user="root",password="",database="employee_attendance_db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM attendance WHERE adate=%s AND e_id=%s", (current_date, employee_id))
        result = cursor.fetchone()

        cursor.close()  # Close the cursor after fetching the result

        if result:
            cursor = conn.cursor()  # Reopen the cursor
            cursor.execute("UPDATE attendance SET outgoing=%s WHERE e_id=%s AND adate=%s", (sign_out_time, employee_id, current_date))
            engine.say("Employee has Sign-out successfully")
            engine.runAndWait()
            
            conn.commit()
            cursor.close()  # Close the cursor after performing the update
            messagebox.showinfo("Success", "Sign-out successful." ,parent=window)
        else:
            engine.say("Employee has not signed in for today.")
            engine.runAndWait()
            messagebox.showwarning("Warning", "Employee has not signed in for today." ,parent=window)

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}" ,parent=window)


def check_employee_id():
    employee_id = id.get()
        
    global efname
    global elname

    # Connect to the MySQL database
    conn = mysql.connector.connect(host="localhost",user="root",password="",database="employee_attendance_db")
    cursor = conn.cursor()
    cursor.execute("SELECT efname, elname FROM employee WHERE e_id = %s", (employee_id,))
    result = cursor.fetchone()

    if result:
        result_label.config(text=" "*70, foreground="green", bg="white")
        employee_exists()
       
        efname, elname = result
        print(efname, " ",elname)

    else:
        if employee_id == "" or employee_id.isspace() :
            result_label.config(text="Please Enter Proper Employee ID", foreground="red")
            engine.say("Please Enter Proper Employee ID")
            engine.runAndWait()
            id.delete(0,END)
        else :
            result_label.config(text="Employee ID does not exist in the database.", foreground="red")
            engine.say("Employee ID does not exist in the database.")
            engine.runAndWait()
            id.delete(0,END)
  
    cursor.close()
    conn.close()

def employee_exists():

    submitbtn=Button(window,text="Sign In",command=sign_in,bg="Green",fg="white",font = ('arial', 15, 'bold'))
    submitbtn.place(x=220,y=280)

    signout=Button(window,text="Sign Out",command=sign_out,bg="Darkorange",fg="white",font = ('arial', 15, 'bold'))
    signout.place(x=350,y=280)


def attend():

    global id, window,result_label

    window=Toplevel()
    window.title('The RiseShine Company')
    window.geometry("670x450+400+130")
    window.resizable(False, False)
    window.configure(background="white")

    window.iconphoto(False, PhotoImage(file = 'icon.png'))

    entire_reg = Frame(window,bd=2,bg="white",relief=RIDGE)
    entire_reg.place(x=30,y=90,width=605,height=300)

    title_add = Frame(window,bd=2,bg="white",relief=RIDGE)
    title_lb1 = Label(window,text="Attendance of Employee",font=("Verdana",30,"bold"),fg="black",bg="white")
    title_lb1.place(x=35,y=4,width=590,height=70)

    title_add.place(x=30,y=2,width=605,height=90)

    #----------id-------------------

    L = Label(window, font = ('arial', 15, 'bold'), text = "Enter Employee id: ",fg="black",bg="white")
    L.place(x = 70, y =130 )

    id=Entry(window,width=20,font =('arial', 15, 'bold'))
    id.place(x=280,y=130)

    # Create a label to display the result
    result_label = Label(window, text="", font=("Arial", 12, "bold"), bg="white")
    result_label.place(x=200,y=170)

    # Create a button to check the employee ID
    check_button = Button(window, text="Check Employee ID", command=check_employee_id,bg="Blue",fg="white",font = ('arial', 13, 'bold'))
    check_button.place(x=250,y=210)

    pass