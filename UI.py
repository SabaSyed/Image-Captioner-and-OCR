from cProfile import label
from distutils.command.config import config
from email import generator
from fileinput import filename
from pydoc import text
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from unittest import result
from cv2 import destroyWindow
from matplotlib import image
import pymysql
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
from tkinter.messagebox import showinfo
import testing_caption_generator as testing
import time
import cv2 

#---------------------------------------------------------------Login Function --------------------------------------
def clear():
    userentry.delete(0,END)
    passentry.delete(0,END)

def close():
    win.destroy()	


def login():
    if user_name.get()=="" or password.get()=="":
        messagebox.showerror("Error","Enter User Name And Password",parent=win)	
    else:
        try:
            con = pymysql.connect(host="localhost",user="root",password="",database="user_fyp")
            cur = con.cursor()

            cur.execute("select * from User_login where username=%s and pass = %s",(user_name.get(),password.get()))
            row = cur.fetchone()

            if row==None:
                messagebox.showerror("Error" , "Invalid User Name And Password", parent = win)

            else:
                messagebox.showinfo("Success" , "Successfully Login" , parent = win)
                close()
                deshboard()
            con.close()
        except Exception as es:
            messagebox.showerror("Error" , f"Error Dui to : {str(es)}", parent = win)

#---------------------------------------------------------------End Login Function ---------------------------------

#---------------------------------------------------- DeshBoard Panel -----------------------------------------
def deshboard():
    global lang, result, captionn
    translator = Translator()

    des = Tk()
    des.title("Home BeMyVision")	
    des.maxsize(width=1200 ,  height=600)
    des.minsize(width=1200 ,  height=600)	

        #heading label
    heading = Label(des , text = f"    Username :  {user_name.get()}    " , font = 'Verdana 20 bold',bg='#373737', fg='#ffffff')
    heading.place(x=270 , y=30)


    heading = Label(des , text = "Caption: " , font = 'Verdana 20 bold')
    heading.place(x=450 , y=100)	


    # lang_ls = Label(des, text= "Select Language:" , font='Verdana 10 bold')
    # lang_ls.place(x=480,y=185)

    # Dropdown menu options
    options = {
        "English":"en",
        "Urdu":"ur",
        "French":"fr",
        "Spanish":"es",
        "Korean":"ko",
        "Arabic":"ar",
        "Italian":"it"
    }
    cap=" "
    label = ttk.Label(text="Select a language:", font=("Arial", 13))
    label.place(x=450,y=185)

    # create a combobox
    selected = tk.StringVar()
    lang_cb = ttk.Combobox(des, textvariable=selected)

    # get languages name
    lang_cb['values'] = ("English","Urdu","French","Spanish","Korean","Arabic","Italian")

    # prevent typing a value
    lang_cb['state'] = 'readonly'

    # place the widget
    lang_cb.place(x=615,y=188)
    lang_cb.current(0)

    label2 = ttk.Label(text='Caption:',width=20, font=("Arial", 13))
    label2.place(x=450,y=218)
    label3 = ttk.Label(text=cap,width=70, font=("Arial", 12))
    label3.place(x=615,y=218)
    label4=ttk.Labelframe(des,width=350,text="Insert an Image",height=350)
    label4.place(x=80,y=100)  
    imagelabel=ttk.Label(label4)
    imagelabel.place(x=0,y=0)  

    

   
    def translatelang(event):
        try:
            lang=options[selected.get()]
            result = translator.translate(label3.cget("text"), dest=lang)
            label3.config(text=result.text)             
        # cap.config(text=result)    
        except:
            print("Error!!!")    

    lang_cb.bind('<<ComboboxSelected>>', translatelang)

    def img_insert():
        global img
        
        try:
            filename = filedialog.askopenfilename(filetypes=(('Jpg Files', '*.jpg')
                                                         ,('Png Files', '*.png')))
            
            rootp = tk.Tk()
            rootp.geometry('300x120')
            rootp.title('Please Wait')

            rootp.grid()

        # progressbar
            pb = ttk.Progressbar(
                rootp,
                orient='horizontal',
                mode='indeterminate',
                length=280)
            pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
            pb.start()
            time.sleep(.1)
            try:
                img=Image.open(filename)
                img_resized=img.resize((350,350)) # new width & height
                img=ImageTk.PhotoImage(img_resized)
                lang=options[selected.get()]
                imagelabel.config(image=img)
                label4.config(text="Image")
                captionn=testing.caption(filename)
            except:
                pb.stop()
            if (lang!='en'):
                captionn = translator.translate(captionn, dest=lang)
                captionn=captionn.text
            label3.config(text=captionn)

            if(label3.cget("text")==captionn):
                pb.stop()
                rootp.destroy()


        except Exception as es:
            messagebox.showerror("Error!" , f"Error Due to : {str(es)}", parent = des)

    def captureimg():
        global img
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Camera")
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                # messagebox.showerror("Error!" , f"Failed to grab Frame.", parent = des)
                print("FAILED")
                break
            cv2.imshow("Camera", frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_{}.jpg".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
                break

        cam.release()
        destroyWindow("Camera")
        try:
            rootp = tk.Tk()
            rootp.geometry('300x120')
            rootp.title('Please Wait')

            rootp.grid()
            pb = ttk.Progressbar(
                rootp,
                orient='horizontal',
                mode='indeterminate',
                length=280)
            pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
            pb.start()
            time.sleep(.1)
            try:
                img=Image.open(img_name)
                img_resized=img.resize((350,350)) # new width & height
                img=ImageTk.PhotoImage(img_resized)
                lang=options[selected.get()]
                imagelabel.config(image=img)
                label4.config(text="Image")
                captionn=testing.caption(img_name)
            except:
                pb.stop()

            if (lang!='en'):
                captionn = translator.translate(captionn, dest=lang)
                captionn=captionn.text
            label3.config(text=captionn)

            if(label3.cget("text")==captionn):
                pb.stop()
                rootp.destroy()
        except:
            print("Couldnt capture image.")

            

    btn_insert= Button(text = "Insert Image" , width = 15, command = img_insert)
    btn_insert.place(x=100, y=470)
    btn_insert= Button(text = "Capture Image" , width = 15, command = captureimg)
    btn_insert.place(x=270, y=470)

    def audio():
        try:
            lang=options[selected.get()]
            myobj = gTTS(text=label3.cget("text"), lang=lang, slow=False)
            myobj.save("caption.mp3")
            playsound('caption.mp3')
        except Exception as es:
            messagebox.showerror("Error!" , f"Error Due to : {str(es)}", parent = des)

    btn_audio = ttk.Button(text='Audio', command=audio)
    btn_audio.place(x=450,y=248)   

    
    

 


        



    
                    
#-----------------------------------------------------End Deshboard Panel -------------------------------------
#----------------------------------------------------------- Signup Window --------------------------------------------------

def signup():
    # signup database connect 
    def action():
        if first_name.get()=="" or last_name.get()=="" or user_name.get()=="" or password.get()=="" or very_pass.get()=="":
            messagebox.showerror("Error" , "All Fields Are Required" , parent = winsignup)
        elif password.get() != very_pass.get():
            messagebox.showerror("Error!" , "Password & Confirm Password Should Be Same." , parent = winsignup)
        else:
            try:
                con = pymysql.connect(host="localhost",user="root",password="",database="user_fyp")
                cur = con.cursor()
                cur.execute("select * from User_login where username=%s",user_name.get())
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error" , "User Name Already Exits", parent = winsignup)
                else:
                    cur.execute("insert into User_login(f_name,l_name,username,pass) values(%s,%s,%s,%s)",
                        (
                        first_name.get(),
                        last_name.get(),
                        user_name.get(),
                        password.get()
                        ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success" , "Registration Successfull!!" , parent = winsignup)
                    clear()
                    switch()
                
            except Exception as es:
                messagebox.showerror("Error!" , f"Error Due to : {str(es)}", parent = winsignup)

    # close signup function			
    def switch():
        winsignup.destroy()

    # clear data function
    def clear():
        first_name.delete(0,END)
        last_name.delete(0,END)
        user_name.delete(0,END)
        password.delete(0,END)
        very_pass.delete(0,END)


    # start Signup Window	
    winsignup = Tk()
    winsignup.title("BeMyVIsion")
    winsignup.maxsize(width=600 ,  height=400)
    winsignup.minsize(width=600 ,  height=400)


    #heading label
    heading = Label(winsignup , text = "Signup" , font = 'Verdana 20 bold')
    heading.place(x=80 , y=60)

    # form data label
    first_name = Label(winsignup, text= "First Name :" , font='Verdana 10 bold')
    first_name.place(x=80,y=130)

    last_name = Label(winsignup, text= "Last Name :" , font='Verdana 10 bold')
    last_name.place(x=80,y=160)

    user_name = Label(winsignup, text= "Username :" , font='Verdana 10 bold')
    user_name.place(x=80,y=190)

    password = Label(winsignup, text= "Password :" , font='Verdana 10 bold')
    password.place(x=80,y=220)

    very_pass = Label(winsignup, text= "Verify Password:" , font='Verdana 10 bold')
    very_pass.place(x=80,y=260)

    # Entry Box ------------------------------------------------------------------

    first_name = StringVar()
    last_name = StringVar()
    user_name = StringVar()
    password = StringVar()
    very_pass = StringVar()


    first_name = Entry(winsignup, width=30 , textvariable = first_name)
    first_name.place(x=230 , y=133)


    last_name = Entry(winsignup, width=30 , textvariable = last_name)
    last_name.place(x=230 , y=163)

    
    user_name = Entry(winsignup, width=30,textvariable = user_name)
    user_name.place(x=230 , y=193)

    
    password = Entry(winsignup, width=30,show="*", textvariable = password)
    password.place(x=230 , y=223)

    
    very_pass= Entry(winsignup, width=30 ,show="*" , textvariable = very_pass)
    very_pass.place(x=230 , y=253)

    # button login and clear

    btn_signup = Button(winsignup, text = "Register" ,font='Verdana 10 bold', command = action)
    btn_signup.place(x=230, y=283)


    btn_login = Button(winsignup, text = "Clear" ,font='Verdana 10 bold' , command = clear)
    btn_login.place(x=360, y=283)


    sign_up_btn = Button(winsignup , text="Already have an account?" , command = switch )
    sign_up_btn.place(x=350 , y =20)


    winsignup.mainloop()
#---------------------------------------------------------------------------End Singup Window-----------------------------------	


    

#------------------------------------------------------------ Login Window -----------------------------------------

win = Tk()

# app title
win.title("BeMyVision")

# window size
win.maxsize(width=600 ,  height=400)
win.minsize(width=600 ,  height=400)


#heading label
heading = Label(win , text = "Login" , font = 'Verdana 25 bold')
heading.place(x=80 , y=150)

username = Label(win, text= "User Name :" , font='Verdana 10 bold')
username.place(x=80,y=220)

userpass = Label(win, text= "Password :" , font='Verdana 10 bold')
userpass.place(x=80,y=260)

# Entry Box
user_name = StringVar()
password = StringVar()
    
userentry = Entry(win, width=30 , textvariable = user_name)
userentry.focus()
userentry.place(x=200 , y=223)

passentry = Entry(win, width=30, show="*" ,textvariable = password)
passentry.place(x=200 , y=260)


# button login and clear

btn_login = Button(win, text = "Login" ,font='Verdana 10 bold',command = login)
btn_login.place(x=200, y=293)


btn_login = Button(win, text = "Clear" ,font='Verdana 10 bold', command = clear)
btn_login.place(x=300, y=293)

# signup button

sign_up_btn = Button(win , text="Register new account " , command = signup )
sign_up_btn.place(x=350 , y =20)



win.mainloop()
