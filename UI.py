from cProfile import label
from distutils.command.config import config
from fileinput import filename
from logging import root
from pydoc import text
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from unittest import result
from cv2 import destroyAllWindows, destroyWindow
from matplotlib import image
from numpy import pad
import pymysql
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
from tkinter.messagebox import showinfo

from torch import hinge_embedding_loss
import testing_caption_generator as testing
import time
import cv2 
# import ocr as ocr



#---------------------------------------------------- DashBoard Panel -----------------------------------------
def deshboard():
    global lang, result, captionn
    translator = Translator()    

    des = Tk()
    des.title("Home")	
    des.maxsize(width=1200 ,  height=700)
    des.minsize(width=1200 ,  height=700)	

    
    f_frame=Frame(des,bg='#FFF', height=700,width=1200)
    f_frame.place(x=0,y=0)

    s_frame=Frame(des,bg='#2e215f', height=70,width=1200)
    s_frame.place(x=0,y=0)

    heading = Label(s_frame , text ="BeMyVision", font = 'Verdana 20 bold', bg='#2e215f', fg='#ffffff')
    heading.place(x=100 , y=30)


        #heading label
    # heading = Label(s_frame , text = f"    Username :  {user_name.get()}    " , font = 'Verdana 20 bold', bg='#2e215f', fg='#ffffff')
    def logout():
        des.destroy()
        loginscreen()
    LogoutBtn = Button(s_frame , text ="Logout", bg='#2e215f', fg='#ffffff',command=logout)
    LogoutBtn.place(x=1100 , y=30)

    cap_heading = Label(f_frame , text = "Caption Generation ",bg='#FFF', font = 'Verdana 20 bold', fg='#2e215f')
    cap_heading.place(x=470 , y=150)	

    # Dropdown menu options
    options = {
     
       "English":"en",
        "Urdu":"ur",
        "French":"fr",
        "Spanish":"es",
        "Korean":"ko",
        "Arabic":"ar",
        "Italian":"it",
        "Bengali":"bn",
        "Chinese":"zh-cn",
        "German":"de",
        "Dutch":"nl",
        "Greek":"el",
        "Persian":"fa",
        "Finnish":"fi",
        "Hindi":"hi",
        "Indonesian":"id",
        "Japanese":"ja",
        "Marathi":"mr",
        "Maltese":"mt",
    }

    cap=" "
    label = Label(f_frame,text="Select a language:", font='Verdana 12 bold', bg='#FFF', fg='#2e215f')
    label.place(x=470,y=235)

    # cbstyle= ttk.Style()
    # cbstyle.theme_use('clam')
    # cbstyle.configure("TCombobox", selectbackground= '#2e215f',foreground=[('readonly','red')], fieldbackground=[('readonly','green')])

    # create a combobox
    selected = tk.StringVar()

    des.option_add("*TCombobox*Listbox*Background", 'white')

    lang_cb = ttk.Combobox(f_frame, textvariable=selected, font = 'Verdana 13 ' )

    # get languages name
    lang_cb['values'] =  (
        "Arabic","Bengali","Chinese","Dutch","English","Finnish","French","German","Greek","Hindi","Indonesian",
        "Italian","Japanese","Korean","Maltese","Marathi","Persian","Spanish","Urdu"
        )


    # prevent typing a value
    lang_cb['state'] = 'readonly'

    # place the widget
    lang_cb.place(x=665,y=238)
    lang_cb.current(0)

    label2 = Label(f_frame,text='Caption:', font = 'Verdana 12 bold', bg='#FFF' , fg='#2e215f')
    label2.place(x=470,y=290)

    label3 = Label(f_frame,text=cap, pady=5, font = 'Verdana 12 ', wraplengt=400 ,width=40,height=3, bg="#FFF",fg='#2e215f' , borderwidth=1, relief="solid")
    label3.place(x=665,y=290)


    frameCnt = 12

    frames = [PhotoImage(file='loading.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

    def update(ind):

        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label_gif.configure(image=frame)
        des.after(100, update, ind)
    label_gif = Label(des, width=200,height=200, bg="#FFF")
    


    des.after(0, update, 0)

    pb = ttk.Progressbar(
        f_frame,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )
    pb.start()

    img_frame=Frame(f_frame,width=350,height=350)
    img_frame.place(x=85,y=150) 

    imagelabel=Label(img_frame,text="Insert an image" , fg="#bebbbb",  font = 'Verdana 20 bold')
    imagelabel.place(x=50,y=150) 

    imagelabel=Label(img_frame)
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

    label2 = Label(f_frame,text='Extracted Text:', font = 'Verdana 12 bold', bg='#FFF', fg='#2e215f')
    label2.place(x=470,y=420)
    label_text =Label(f_frame, font = 'Verdana 12', wraplengt=450 ,width=40,height=3, bg="#FFF", fg='#2e215f' , borderwidth=1, relief="solid")
    label_text.place(x=665,y=420)    

    def img_insert():
        global img

        try:
            # pb.place(x=720,y=380)
            filename = filedialog.askopenfilename(filetypes=(('Jpg Files', '*.jpg')
                                                         ,('Png Files', '*.png')))
            
            img=Image.open(filename)
            img_resized=img.resize((350,350)) # new width & height
            img=ImageTk.PhotoImage(img_resized)
            imagelabel.config(image=img)

        except Exception as es:
            messagebox.showerror("Error!" , f"Error Due to : {str(es)}", parent = des)
 
        try:
            label_gif.place(x=470,y=200)

            lang=options[selected.get()]
            captionn=testing.caption(filename)
            
            if (lang!='en'):
                captionn = translator.translate(captionn, dest=lang)
                captionn=captionn.text
            label3.config(text=captionn)
            # time.sleep(5)
            # texts=ocr.Text(filename)
            # print(filename)
            # label_text.config(text=texts)
            pb.place_forget()
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
                messagebox.showerror("Error!" , f"Failed to grab Frame.", parent = des)
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
                filename = "opencv_frame_{}.jpg".format(img_counter)
                cv2.imwrite(filename, frame)
                print("{} written!".format(filename))
                img_counter += 1
                break

        cam.release()
        destroyWindow("Camera")
        try:
            try:
                img=Image.open(filename)
                img_resized=img.resize((350,350)) # new width & height
                img=ImageTk.PhotoImage(img_resized)
                lang=options[selected.get()]
                imagelabel.config(image=img)
                captionn=testing.caption(filename)
            except:
                print("Inner exception")

            if (lang!='en'):
                captionn = translator.translate(captionn, dest=lang)
                captionn=captionn.text
            label3.config(text=captionn)

            # try:
            #     texts=ocr.Text(filename)
            #     print(filename)
            #     label_text.config(text=texts)
            # except Exception as es:
            #     messagebox.showerror("Error!" , f"Error Due to : {str(es)}", parent = des)
        except:
            print("Couldnt capture image.")

            

    btn_insert= Button(f_frame,text = "Insert Image" , width = 15, command = img_insert, bg='#2e215f',fg='#FFF', pady=6)
    btn_insert.place(x=100, y=520)
    btn_insert= Button(f_frame,text = "Capture Image" , width = 15, command = captureimg, fg='#FFF' , bg='#2e215f',pady=6)
    btn_insert.place(x=270, y=520)

    def audio():
        try:
            lang=options[selected.get()]
            myobj = gTTS(text=label3.cget("text"), lang=lang, slow=False)
            myobj.save("caption.mp3")
            playsound('caption.mp3')
        except Exception as es:
            messagebox.showerror("Error!" , f"Error Due to : {str(es)}", parent = des)

    # btn_audio = Button(f_frame, command=audio, text="Audio", pady=6, fg="#FFF", bg='#2e215f' )
    global photo
    photo= Image.open("speaker.png")
    newsize = (30, 30)
    img_btn = photo.resize(newsize)
    photo = ImageTk.PhotoImage(img_btn) 

    # Add image to button
    btn_audio = Button(des, image=photo, command=audio, text=" ", bg="#FFF" , border = '0')
    btn_audio.place(x=1080,y=300) 


    

 

    
                    
#-----------------------------------------------------End Dashboard Panel -------------------------------------
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
        loginscreen()

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
    winsignup.maxsize(width=1200 ,  height=650)
    winsignup.minsize(width=1200 ,  height=650)

    s_frame=Frame(winsignup,bg='#2e215f', height=700,width=600)
    s_frame.place(x=600,y=0)

    
    heading = Label(s_frame,bg='#2e215f' , fg="#FFF" , text = "BeMyVision" , font = 'Verdana 22 bold')
    heading.place(x=70 , y=60)

    # form data label
    SubHeading = Label(s_frame,bg='#2e215f', fg="#FFF" , text= "Image Captioning system using CNN LSTM" , font='Verdana 12 ')
    SubHeading.place(x=70,y=90)

    intro = Label(s_frame,bg='#2e215f', fg="#FFF" , wraplengt=500 , text= "Lorem ipsum dolor sit amet. Non molestias minima et aliquid iure rem possimus quae et explicabo nulla qui dolores deleniti eos enim assumenda. Et quia velit ad dolores molestiae ut commodi quos et veritatis recusandae qui voluptates illo et similique voluptatem! Vel dolor iusto ea temporibus enim hic culpa voluptatem aut blanditiis saepe aut sequi tempore et doloremque dolore! Non excepturi delectus ab quasi accusamus est pariatur cupiditate est illo cupiditate ab laudantium dolores sed assumenda illum vel voluptas assumenda. " , font='Verdana 12 ')
    intro.place(x=70,y=200)



    f_frame=Frame(winsignup,bg='#FFF', height=700,width=600)
    f_frame.place(x=0,y=0)
    #heading label
    heading = Label(f_frame,bg='#FFF' , fg="#2e215f" , text = "Signup" , font = 'Verdana 22 bold')
    heading.place(x=70 , y=70)

    # form data label
    first_name = Label(f_frame,bg='#FFF', fg="#2e215f" , text= "First Name :" , font='Verdana 12 ')
    first_name.place(x=70,y=150)

    last_name = Label(f_frame,bg='#FFF', fg="#2e215f" , text= "Last Name :" , font='Verdana 12 ')
    last_name.place(x=70,y=200)

    user_name = Label(f_frame,bg='#FFF', fg="#2e215f" , text= "Username :" , font='Verdana 12 ')
    user_name.place(x=70,y=250)

    password = Label(f_frame ,bg='#FFF', fg="#2e215f" , text= "Password :" , font='Verdana 12 ')
    password.place(x=70,y=300)

    very_pass = Label(f_frame,bg='#FFF', fg="#2e215f" , text= "Confirm Password:" , font='Verdana 12 ')
    very_pass.place(x=70,y=350)

    # Entry Box ------------------------------------------------------------------

    first_name = StringVar()
    last_name = StringVar()
    user_name = StringVar()
    password = StringVar()
    very_pass = StringVar()


    first_name = Entry(f_frame,bg='#FFF', width=30 , textvariable = first_name)
    first_name.place(x=270 , y=155)


    last_name = Entry(f_frame, width=30,bg='#FFF' , textvariable = last_name)
    last_name.place(x=270 , y=205)

    
    user_name = Entry(f_frame,bg='#FFF', width=30,textvariable = user_name)
    user_name.place(x=270 , y=255)

    
    password = Entry(f_frame,bg='#FFF', width=30,show="*", textvariable = password)
    password.place(x=270 , y=305)

    
    very_pass= Entry(f_frame,bg='#FFF', width=30 ,show="*" , textvariable = very_pass)
    very_pass.place(x=270 , y=355)

    # button login and clear

    btn_signup = Button(f_frame,bg='#2e215f',fg="#FFF",border="0" ,pady=5, width=10, text = "Register" ,font='Verdana 10 bold', command = action)
    btn_signup.place(x=150, y=425)


    btn_login = Button(f_frame,bg='#2e215f',fg="#FFF",border="0" ,pady=5,width=10,  text = "Clear" ,font='Verdana 10 bold' , command = clear)
    btn_login.place(x=290, y=425)


    sign_up_btn = Button(f_frame ,bg='#2e215f',width=25, fg="#FFF",border="0" ,pady=6, text="Already have an account?" ,font='Verdana 10 bold', command = switch )
    sign_up_btn.place(x=150 , y =475)




    winsignup.mainloop()
#---------------------------------------------------------------------------End Singup Window-----------------------------------	


#------------------------------------------------------------ Login Window -----------------------------------------
def loginscreen():
    def opensignup():
        win.destroy()
        signup()
    def clear():
        userentry.delete(0,END)
        passentry.delete(0,END)

    def close():
        win.destroy()	
#---------------------------------------------------------------Login Function --------------------------------------

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

    win = Tk()

    # app title
    win.title("BeMyVision")

    # window size
    win.maxsize(width=1100 ,  height=600)
    win.minsize(width=1100 ,  height=600)


    f_frame=Frame(win,bg='#FFF', height=600,width=500)
    f_frame.place(x=0,y=0)

    s_frame=Frame(win,bg='#2e215f', height=600,width=600)
    s_frame.place(x=500,y=0)

    heading = Label(s_frame,bg='#2e215f' , fg="#FFF" , text = "BeMyVision" , font = 'Verdana 22 bold')
    heading.place(x=70 , y=60)

    # form data label
    SubHeading = Label(s_frame,bg='#2e215f', fg="#FFF" , text= "Image Captioning system using CNN LSTM" , font='Verdana 12 ')
    SubHeading.place(x=70,y=90)

    intro = Label(s_frame,bg='#2e215f', fg="#FFF" , wraplengt=500 , text= "Lorem ipsum dolor sit amet. Non molestias minima et aliquid iure rem possimus quae et explicabo nulla qui dolores deleniti eos enim assumenda. Et quia velit ad dolores molestiae ut commodi quos et veritatis recusandae qui voluptates illo et similique voluptatem! Vel dolor iusto ea temporibus enim hic culpa voluptatem aut blanditiis saepe aut sequi tempore et doloremque dolore! Non excepturi delectus ab quasi accusamus est pariatur cupiditate est illo cupiditate ab laudantium dolores sed assumenda illum vel voluptas assumenda. " , font='Verdana 12 ')
    intro.place(x=70,y=200)



    #heading label
    heading = Label(win , text = "Login", bg='#FFF', fg="#2e215f" ,  font = 'Verdana 25 bold ')
    heading.place(x=80 , y=150)

    username = Label(win, text= "User Name :" , bg='#FFF', fg="#2e215f" , font='Verdana 10 ')
    username.place(x=80,y=220)

    userpass = Label(win, text= "Password :" , bg='#FFF', fg="#2e215f" , font='Verdana 10 ')
    userpass.place(x=80,y=270)

    # Entry Box
    user_name = StringVar()
    password = StringVar()
        
    userentry = Entry(win, width=30 , textvariable = user_name)
    userentry.focus()
    userentry.place(x=200 , y=220)

    passentry = Entry(win, width=30, show="*" ,textvariable = password)
    passentry.place(x=200 , y=270)


    # button login and clear

    btn_login = Button(win, text = "Login" , bg='#2e215f',width=10, fg="#FFF",border="0" ,pady=6,font='Verdana 10 bold',command = login)
    btn_login.place(x=150, y=350)


    btn_clear = Button(win, text = "Clear" ,bg='#2e215f',width=10, fg="#FFF",border="0" ,pady=6,font='Verdana 10 bold', command = clear)
    btn_clear.place(x=285, y=350)

    # signup button

    sign_up_btn = Button(win ,bg='#2e215f',width=25, fg="#FFF",border="0" ,pady=6, text="Register new account " ,font='Verdana 10 bold', command = opensignup )
    sign_up_btn.place(x=150 , y =400)



    win.mainloop()


loginscreen()
