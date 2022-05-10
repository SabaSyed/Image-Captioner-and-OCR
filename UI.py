from cProfile import label
from distutils.command.config import config
from email import generator
from fileinput import filename
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from unittest import result
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
    global lang, result
    translator = Translator()

    des = Tk()
    des.title("Home BeMyVision")	
    des.maxsize(width=1200 ,  height=600)
    des.minsize(width=1200 ,  height=600)	

        #heading label
    heading = Label(des , text = f"    Username :  {user_name.get()}    " , font = 'Verdana 20 bold',bg='#373737', fg='#ffffff')
    heading.place(x=270 , y=30)

    f=Frame(des,height=350,width=350,bg="#FFF")
    f.place(x=80,y=100)


    # Book Docter Appointment App
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
    cap="This is an example caption"
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

    label2 = ttk.Label(text='Caption:',width=20, font=("Arial", 13))
    label2.place(x=450,y=218)
    label3 = ttk.Label(text=cap,width=70, font=("Arial", 12))
    label3.place(x=615,y=218)
   
    def translatelang(event):
        lang=options[selected.get()]
        result = translator.translate(label3.cget("text"), dest=lang)
        label3.config(text=result.text)             
        # cap.config(text=result)        
    lang_cb.bind('<<ComboboxSelected>>', translatelang)

    def img_insert():
        lang='en'
        f_types = [('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        img=Image.open(filename)
          
        captionn=testing.caption(filename)
        label3.config(text=captionn)

        img_resized=img.resize((350,350)) # new width & height
        img=ImageTk.PhotoImage(img_resized)
        label4=ttk.Label(des,image=img)
        label4.place(x=80,y=100)  


    btn_insert= Button(text = "Insert Image" , width = 20, command = img_insert)
    btn_insert.place(x=150, y=470)

    def audio():
        lang=options[selected.get()]
        myobj = gTTS(text=label3.cget("text"), lang=lang, slow=False)
        myobj.save("caption.mp3")
        playsound('caption.mp3')

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
