from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

def viewAttendance():
    global id, filter_var, data_listbox, data_label, window
    
    window = Toplevel()
    window.title('The RiseShine Company')
    window.geometry("1140x658+230+50")
    window.configure(bg="#e9fcd7")
    window.resizable(False, False)

    window.iconphoto(False, PhotoImage(file = 'icon.png'))

    #canvas to hold the table and scrollbar
    canvas = Canvas(window)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    #Frame to hold the table
    table_frame = Frame(canvas)
    canvas.create_window((0, 0), window=table_frame, anchor='nw')

    #vertical scrollbar
    scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure the Canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    greet = Label(table_frame, font=('verdana', 30, 'bold'), bg="white", padx=0, pady=20, text="Employee Attendance Sheet", width=40)
    greet.grid(row=0, columnspan=7)

    db = mysql.connector.connect(host="localhost", user="root", password='', database='employee_attendance_db')
    cursor = db.cursor()

    sqlquery = "SELECT * FROM attendance;"
    print(sqlquery)

    try:
        cursor.execute(sqlquery)
        rows = cursor.fetchall()

        num_columns = 8  
        for i in range(num_columns):
            table_frame.grid_columnconfigure(i, weight=1)

        # Function to create cell borders
        def create_border(row, column, border_color="#95c261"):
            frame = Frame(table_frame, bd=1, relief="solid")
            frame.grid(row=row, column=column, sticky="nsew")
            frame.config(highlightbackground=border_color)
            return frame
    
        # Create headers
        headers = ["Date", "ID", "First Name","Last Name","Status", "Sign In", "Outgoing"]
        for i, header in enumerate(headers):
            header_frame = create_border(2, i)
            header_label = Label(header_frame, text=header, font=('verdana', 15, 'bold'), padx=0, pady=15, bg="#dafcb3")
            header_label.pack(fill="both", expand=True)

        # Populate the table with data and borders
        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):                
                cell_frame = create_border(row_idx + 6, col_idx)
                cell_label = Label(cell_frame, text=cell_data, font=('verdana', 15), padx=0, pady=13, bg="white")
                cell_label.pack(fill="both", expand=True)

    except:
        messagebox.showinfo("Error", "Cannot Fetch data." ,parent=window)

    # Update the Canvas scroll region
    table_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    window.mainloop()