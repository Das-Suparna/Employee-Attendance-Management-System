from tkinter import *
import mysql.connector
from add import *
from attendance import * 
from show_attendance import *
from view import *
from PIL import Image,ImageTk

window=Tk()
window.title("The RiseShine Company")
window.configure(background="white")
window.state('zoomed')
window.resizable(False, False)

window.iconphoto(False, PhotoImage(file = 'icon.png'))

title_lb1 = Label(window,text="EMPLOYEE ATTENDANCE MANAGEMENT SYSTEM",font=("Verdana",30,"bold"),fg="black",bg="white")
title_lb1.place(x=220,y=30,width=1100,height=50)  

#register button

image_path = "D:\Python Employee Attendance Proj\images\home1.png" 
desired_size = (400, 290)
image = Image.open(image_path)
image = image.resize(desired_size, Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

label = Label(window, bg="white")
label.image = photo  
label.config(image=photo)  
label.place(x=40, y=180, width=300, height=250)

addbtn=Button(window,text="Employee Register",command=addEmp,bg="blue",fg="white",font = ('arial', 22, 'bold'))
addbtn.place(x=40, y=510, width=300, height=50)


#attendance mark

url2 = "D:\Python Employee Attendance Proj\images\home2.png"
image2 = Image.open(url2)
desired_size = (380, 360)
image2 = image2.resize(desired_size, Image.LANCZOS)
photo = ImageTk.PhotoImage(image2)

label = Label(window)
label.image2 = photo 
label.config(image=photo)  
label.place(x=420, y=170, width=300, height=270)

issuebtn=Button(window,text="Attendance Mark",command=attend,bg="blue",fg="white",font = ('arial', 22, 'bold'))
issuebtn.place(x=420, y=510, width=300, height=50)


#view edit attendance 

url3 = "D:\Python Employee Attendance Proj\images\home3.png"
image2 = Image.open(url3)
desired_size = (400, 350)
image2 = image2.resize(desired_size, Image.LANCZOS)
photo = ImageTk.PhotoImage(image2)

label = Label(window)
label.image2 = photo  
label.config(image=photo)  
label.place(x=800, y=170, width=320, height=270)

viewbtn=Button(window,text="View Employee",command=viewEmployee,bg="blue",fg="white",font = ('arial', 22, 'bold'))
viewbtn.place(x=800, y=510, width=300, height=50)


# view attendance
url4 = "D:\Python Employee Attendance Proj\images\home4.png"
image2 = Image.open(url4)
desired_size = (370, 300)
image2 = image2.resize(desired_size, Image.LANCZOS)
photo = ImageTk.PhotoImage(image2)

label = Label(window)
label.image2 = photo  
label.config(image=photo)  
label.place(x=1120, y=170, width=400, height=300)

viewbtn=Button(window,text="View Attendance",command=viewAttendance,bg="blue",fg="white",font = ('arial', 22, 'bold'))
viewbtn.place(x=1150, y=510, width=350, height=50)


viewbtn=Button(window,text="Exit",command=exit,bg="red",fg="white",font = ('arial', 22, 'bold'))
viewbtn.place(x=700, y=630, width=100, height=50)



window.mainloop()




def exit():
    window.destroy()
    add.destroy()
    attendance.destroy()
    view.destroy()
    show_attendance.destroy()