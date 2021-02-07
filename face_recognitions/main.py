import serial                    # == 3.5
import time                      # standard packges
import datetime                  # standard packges
import pyttsx3                   # == 2.90
import face_recognition          # == 1.3.0,cmake == 3.18.4.post1, dlib == 19.8.1
import cv2                       # == opencv-contrib-python 4.4.0.46
import pandas as pd              # == 1.1.5
import numpy as np               # == 1.19.4
import os                        # standard packages
import tkinter as tk 
from tkinter import * 
import PIL.Image
import PIL.ImageTk
from threading import Thread 
import sqlite3   

################################################################################################################################################################################

#  This object and var is for collect anf detect mode 
scaleVal = 1 + (300/1000)                                                             # (1) Param for Haar sacade face detect in collect function
neig = 6                                                                              # (1) Param for Haar sacade face detect in collect function
minArea = 10                                                                          # (1) Param for Haar sacade face detect in detect function, condition to draw bounding box
thresh_x = 70                                                                         # (1) Param for Haar sacade face detect in detect function, condition to draw bounding box
thresh_y = 100                                                                        # (1) Param for Haar sacade face detect in detect function, condition to draw bounding box
accept_distance  = 0.4
enable_collect = False                                                                # (1) This bit is use for control the collect mode
roi_face = np.array([])                                                               # (1) This is for face detected and save this to folder face id
photo  = None                                                                         # (1) Really important for reading frame  in collect window have to be IN main
photo1 = None                                                                         # (1) Really important for reading frame  in collect window have to be IN main
cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)                                              # (1) Make a connect Camera In
cap2 = cv2.VideoCapture(1,cv2.CAP_DSHOW)                                              # (1) Make a connection to Camera Out

# Get location and encoding this roi_face for detect function
face_locations_in  = []                                                               # This is use for detect function, global var for create thread in
face_encodings_in  = []                                                               # This is use for detect function, global var for create thread in
face_locations_out = []                                                               # This is use for detect function, global var for create thread out
face_encodings_out = []                                                               # This is use for detect function, global var for create thread out

path_icon = "./ICON_file/"                                                            # Path store icon for build app
path_xml  = r"./haarcascade_frontalface_default.xml"                                  # Path store haar cascade file for learn face function
path_id   = r"./face_Id"                                                              # Path store all face learned
path_unknown  = "./face_Unknown/"                                                     # Path store unknown faces
path_known    = "./face_Known/"                                                       # Path store known faces
path_csv      = "./csv_Daily/"                                                        # (2) Path store CSV file            GLOBAL in function CHECK,ADD_IN,OUT at window DETECT
path_db       = "./DB_Daily/"                                                         # (2) Path store Database file       GLOBAL in function CHECK,ADD_IN,OUT at window DETECT
file_name_csv = str("")                                                               # (2) Using for named file csv       GLOBAL in function CHECK,ADD_IN,OUT at window DETECT
file_name_db  = str("")                                                               # (2) Using for named file db        GLOBAL in function CHECK,ADD_IN,OUT at window DETECT
df            = pd.DataFrame(None,columns = ["Name","Date","Time","Type","Distance"]) # (2) This is dataframe              GLOBAL in function CHECK,ADD_IN,OUT at window DETECT
conn          = None                                                                  # (2) This is sql connect object for GLOBAL in function CHECK,ADD_IN,OUT at window DETECT
#
name_in       = str("")                                                               # (3) Add in function
name_out      = str("")                                                               # (3) Add out function
name_in_prev  = str("")                                                               # (3) Add in function
name_out_prev = str("")                                                               # (3) Add out function
dis_in        = 0.0                                                                   # (3) Add in function
dis_out       = 0.0                                                                   # (3) Add out function

# Create Jennis
Jennis = pyttsx3.init()                # crate Jennis
Jennis.setProperty("rate",165)         # Seting speed volume
Jennis.say("Hello my name is Jennis, Nice to meet you!")
Jennis.runAndWait()

################################################################################################################################################################################

# This function is using to support face_list function, to find the name in image path
def find_name(path):

    end_index  = path.index(".jpg")
    start_index = path.index("\\")

    return path[start_index+1:end_index]

# This function collect all face in folder face_ID and create a name list and face encoding list in path_id
def face_list(path):
    
    known_face_paths     = []                               # list of known path
    known_face_names     = []                               # list of known names      
    known_face_encodings = []                               # list of encodings
    known_face_images    = []                               # list of known faces
    dirs = os.listdir(path)

    for direc in dirs:
        img_path = os.path.join(path,direc)                 # Read img path
        known_face_paths.append(img_path)                   # Append img path
        face = face_recognition.load_image_file(img_path)   # Read img in img_path
        known_face_images.append(face)                      # Append images face
        encoding = face_recognition.face_encodings(face)[0] # Encoding face
        known_face_encodings.append(encoding)               # Append encoding list
        name = find_name(img_path)                          # Find name of image
        known_face_names.append(name)                       # Append name to name list
        
    return known_face_names,known_face_encodings

#This function is using to create database and dataframe
def funct_datacreate():

    global path_csv, path_db, file_name_db, file_name_csv, conn, df

    t= datetime.datetime.now()
    time_name =str(t)[0:10].replace(":","-")     # Change your time index here
    file_name_csv = "VVSAC_" + time_name + ".csv"
    file_name_db  = "VVSAC_" + time_name + ".db"
    print(str(datetime.datetime.now()) + " CHECKING DATA...")
    
    #Create Dataframe
    if not os.path.exists(path_csv + file_name_csv):
        data = None
        df = pd.DataFrame( data,columns = ["Name","Date","Time","Type","Distance"] )
        df.to_csv(path_csv + file_name_csv)
        print(file_name_csv + " : Created!")

    else:
        print(file_name_csv + " Already!")
        df = pd.read_csv(path_csv + file_name_csv)

    if not os.path.exists(path_db + file_name_db):
        conn = sqlite3.connect(path_db + file_name_db)
        c = conn.cursor()
        #Create table could be make mistake if you table allready there
        c.execute("""
                    CREATE TABLE table_io 
                    (Name TEXT,
                     Date TEXT, 
                     Time TEXT,
                     Type TEXT, 
                     Distance REAL)
                     """)
        conn.commit()  
        conn.close()
        print(file_name_db +  "  : Created!")
    else:
        print(file_name_db + " Already!")
    return

#This function is using to communicate with
def sendByte(a,device_port):
    
    device_port.write(chr(a).encode("ascii"))

################################################################################################################################################################################
# Button function
def func_collect():

    global path_icon,path_xml,enable_collect,photo # go to (1)

    #Setup something first
    cascade = cv2.CascadeClassifier(path_xml)
    #Reset your enable collect mode 
    enable_collect = False

    #Label on home screen
    label_mode.config(text  = "Collect Mode Activated")

    #Create a window
    window_collect = tk.Toplevel()
    window_collect.geometry("1105x667")
    window_collect.title("Collect Window")
    window_collect.iconbitmap(path_icon +"VVS_logo.ico")
    window_collect.resizable(width = False,height = False)

    #Define background
    bg_collect = PIL.ImageTk.PhotoImage(file = path_icon + "collect1.png")

    #Define  Canvas
    my_canvas = tk.Canvas(window_collect,width = 1105, height = 667, bd = 0, highlightthickness = 0)
    my_canvas.pack(fill = "both", expand = True)

    #Put the image background into canvas
    my_canvas.create_image(0,0,image = bg_collect, anchor = "nw")
    
    #Define the entry box and more element
    un_entry      = tk.Entry(window_collect, font = ("Heivetica",24),width = 14,fg = "#336d92", bd = 0)
    pw_entry      = tk.Entry(window_collect, font = ("Heivetica",24),width = 14,fg = "#336d92", bd = 0)
    name_entry    = tk.Entry(window_collect, font = ("Heivetica",24),width = 20,fg = "#336d92", bd = 0)
    name_label    = tk.Label(window_collect, text = "Face's name",fg = "red", font = ("Arial",24))
    cam_label     = tk.Label(window_collect, text = "Camera view",fg = "green", font = ("Arial",24))
    face_label    = tk.Label(window_collect, text = "Learning face",fg = "green", font = ("Arial",24))
    confirm_label = tk.Label(window_collect, text = "Detecting",fg = "blue", font = ("Arial",20))
    
    def handlename():
        confirm_label.configure(text = "Detecting")
        name_label.configure(text = name_entry.get() + ".jpg")

    button_check = tk.Button(window_collect,text = "Check name", command = handlename)

    def handlesave():

        global path_id,roi_face

        print(str(datetime.datetime.now()) + " SAVING NEW IMAGE...")

        image_name = path_id + "/" + name_label["text"]
        #print(image_name)
        cv2.imwrite(image_name,roi_face)
        confirm_label.configure(text = "Done!")

    button_save = tk.Button(window_collect,text = "Save it", command = handlesave)

    #Set current text for pass in
    un_entry.insert(0,"username")
    pw_entry.insert(0,"password")

    #Create canvas window before enable entry
    un_window = my_canvas.create_window(400,200,anchor  = "nw", window = un_entry)
    pw_window = my_canvas.create_window(400,250,anchor = "nw", window = pw_entry)

    #Create entry function
    #This function use for checkin
    def checkin():
        
        global enable_collect

        if (un_entry.get() == "admin") and ( pw_entry.get() == "w5" ):
            un_entry.destroy()
            pw_entry.destroy()
            button_login.destroy()
            enable_collect = True    # Turn on enable collect mode

    #This function is use for entry box clear function
    def entry_clear(e):
        if ( un_entry.get() == "username" ) or ( pw_entry.get() == "password" ):
            un_entry.delete(0,END)
            pw_entry.delete(0,END)

            #change text to stars
            pw_entry.config(show = "*")

    #Canvas pack
    button_login = tk.Button(window_collect, text = "Login",font = ("Helvetica",20),width = 14, fg = "#336d92", command = checkin)
    button_login_window = my_canvas.create_window(410,350,anchor = "nw",window = button_login)

    #Bind entry boxes
    un_entry.bind("<Button-1>",entry_clear)
    pw_entry.bind("<Button-1>",entry_clear)

    def update(period = 1000):

        global enable_collect,cap2,photo,photo1,scaleVal,neig,minArea,thresh_y,thresh_x,roi_face

        #print(enable_collect)
        if enable_collect:
            ret,frame = cap2.read()
            frame_copy = frame.copy()
            
            #Get your image convert to gray scale
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

            #Detect object face
            objects = cascade.detectMultiScale(gray,scaleVal,neig)

            #Draw bounding box for each face in bouding box
            for (x,y,w,h) in objects:
                area = w * h
                if area >minArea:
                    try:
                        #Take your ROI_FACE out of frame
                        roi_face = frame_copy[y-thresh_y:y+h+thresh_y,x-thresh_x:x+w+thresh_x]
                        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        frame = cv2.putText(frame,"learn face",(x,y-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),1)
                    except: pass

            #Convert
            #Sometime just dont have any roi_face so you have to put it into try
            try:
                roi_inv   = cv2.cvtColor(roi_face,cv2.COLOR_BGR2RGB)
                photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(roi_inv))
                my_canvas.create_image(700,10,image = photo1, anchor = tk.NW)
            except: pass

            #invert for tkinter
            frame_inv = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            photo = PIL.ImageTk.PhotoImage(image  = PIL.Image.fromarray(frame_inv))
            
            # Draw canvas after entry
            my_canvas.create_window(10,550,anchor  = "nw", window = name_entry)
            my_canvas.create_window(450,560,anchor = "nw", window = button_check)
            my_canvas.create_window(600,550,anchor = "nw", window = name_label)
            my_canvas.create_window(900,600,anchor = "nw", window = button_save)
            my_canvas.create_window(950,600,anchor = "nw", window = confirm_label)

            my_canvas.create_window(750,500,anchor = "nw", window = face_label)
            my_canvas.create_window(250,500,anchor = "nw", window = cam_label)
            
            my_canvas.create_image(10,10,image = photo, anchor = tk.NW)

        window_collect.after(period,update) # Update after xxxx ms

    update()                  #Update function
    
    window_collect.mainloop() #Loop your window if you dont do this, something go wrong, like your canvas

def func_detect():

    global path_icon,photo,photo1,path_id,path_unknown,path_known

    #Label on home screen
    label_mode.config(text  = "Detect Mode Activated")

    #Create a window
    window_detect = tk.Toplevel()
    window_detect.geometry("1302x681")
    window_detect.title("Detect Window")
    window_detect.iconbitmap(path_icon +"VVS_logo.ico")
    window_detect.resizable(width = False,height = False)

    #Define background
    bg_collect = PIL.ImageTk.PhotoImage(file = path_icon + "detect1.png")

    #Define Canvas
    my_canvas = tk.Canvas(window_detect,width = 1302, height = 681, bd = 0, highlightthickness = 0)
    my_canvas.pack(fill = "both", expand = True)

    #Put background into your canvas
    my_canvas.create_image(0,0,image = bg_collect, anchor = "nw")

    # Read all your face in face_Id floder and encode it
    known_face_names,known_face_encodings = face_list(path_id)

    #Draw Label Camera

    camera_in_label    = tk.Label(window_detect, text = "Camera in"  ,fg = "green", font = ("Arial",16))
    camera_out_label   = tk.Label(window_detect, text = "Camera out" ,fg = "green", font = ("Arial",16))
    namein_prev_label  = tk.Label(window_detect, text = "In prev"    ,fg = "green", font = ("Arial",16))
    namein_label       = tk.Label(window_detect, text = "In Now"     ,fg = "green", font = ("Arial",16))
    nameout_prev_label = tk.Label(window_detect, text = "Out prev"   ,fg = "green", font = ("Arial",16))
    nameout_label      = tk.Label(window_detect, text = "Out Now"    ,fg = "green", font = ("Arial",16))
    valin_prev         = tk.Label(window_detect, text = "In prev"    ,fg = "red"  , font = ("Arial",16))
    valin_now          = tk.Label(window_detect, text = "In now"     ,fg = "red"  , font = ("Arial",16))
    valout_prev        = tk.Label(window_detect, text = "Out prev"   ,fg = "red"  , font = ("Arial",16))
    valout_now         = tk.Label(window_detect, text = "Out now"    ,fg = "red"  , font = ("Arial",16))

    my_canvas.create_window(250,520,anchor = "nw", window = camera_in_label)
    my_canvas.create_window(100,570,anchor = "nw", window = namein_prev_label)
    my_canvas.create_window(300,570,anchor = "nw", window = valin_prev)
    my_canvas.create_window(100,620,anchor = "nw", window = namein_label)
    my_canvas.create_window(300,620,anchor = "nw", window = valin_now)

    my_canvas.create_window(900,520,anchor = "nw", window = camera_out_label)
    my_canvas.create_window(750,570,anchor = "nw", window = nameout_prev_label)
    my_canvas.create_window(950,570,anchor = "nw", window = valout_prev)
    my_canvas.create_window(750,620,anchor = "nw", window = nameout_label)
    my_canvas.create_window(950,620,anchor = "nw", window = valout_now)

    #Check dataframe and database function
    def check():
        
        global path_csv, path_db, file_name_db, file_name_csv, conn, df

        #print(str(datetime.datetime.now()) + " CHECKING DATA...")

        t = datetime.datetime.now()
        time_name_now  = str(t)[0:10].replace(":","-")     # Change your time index here
        time_name_prev = file_name_csv[6:16]                # Change your time index here

        if time_name_now != time_name_prev:

            #Read time first
            t = datetime.datetime.now()
            time_name =str(t)[0:10].replace(":","-")     # Change your time index here
            file_name_csv = "VVSAC_" + time_name + ".csv"
            file_name_db  = "VVSAC_" + time_name + ".db"

            #Create Dataframe
            data      = None 
            df        = pd.DataFrame(data, columns = ["Name","Date","Time","Type","Distance"])
            df.to_csv(path_csv + file_name_csv)

            #Create Database
            conn = sqlite3.connect(path_db + file_name_db)
            c    = conn.cursor()

            #Create table could be make mistake if you table already there
            c.execute("""
                CREATE TABLE table_io 
                (Name TEXT,
                 Date TEXT, 
                 Time TEXT,
                 Type TEXT, 
                 Distance REAL)
                 """) 
            conn.commit()
            conn.close()

            print(str(datetime.datetime.now()) + " CREATING DATA...")
            print("time_name: " + time_name)
            print(file_name_csv + " : Created! ")
            print(file_name_db + " : Created! ")
    
    #Add new data in function
    def add_in():

        global path_csv, path_db, file_name_csv, file_name_db, conn, df, name_in,dis_in

        t = datetime.datetime.now()
        time_now = str(t)
        
        #Value add to dataframe and database
        date_clock = time_now[0:10]
        time_clock = time_now[11:-1]
        name = name_in
        typ = "In"
        dis = dis_in

        #Add dataframe
        df1  = pd.DataFrame({"Name":[name],"Date":[date_clock],"Time":[time_clock],"Type":[typ],"Distance":[dis]})
        df   = df.append(df1)
        df.reset_index(drop = True, inplace= True)
        df.to_csv(path_csv + file_name_csv)
        
        #Add database
        data_row = (name,date_clock,time_clock,typ,dis)
        conn = sqlite3.connect(path_db + file_name_db)
        c = conn.cursor()
        c.execute("INSERT INTO table_io VALUES (?,?,?,?,?)",data_row)
        conn.commit()
        conn.close()
        
        #print("Data"+ str(data_row) +" In Added!")

        return
    
    #Add new data out function
    def add_out():

        global path_csv, path_db, file_name_csv, file_name_db, conn, df, name_out,dis_out

        t = datetime.datetime.now()
        time_now = str(t)

        #Value add to dataframe and database
        date_clock = time_now[0:10]
        time_clock = time_now[11:-1]
        name = name_out
        typ = "Out"
        dis = dis_out

        #Add dataframe
        df1  = pd.DataFrame({"Name":[name],"Date":[date_clock],"Time":[time_clock],"Type":[typ],"Distance":[dis]})
        df   = df.append(df1)
        df.reset_index(drop = True, inplace= True)
        df.to_csv(path_csv + file_name_csv)

        #Add database
        data_row = (name,date_clock,time_clock,typ,dis)
        conn = sqlite3.connect(path_db + file_name_db)
        c = conn.cursor()
        c.execute("INSERT INTO table_io VALUES (?,?,?,?,?)",data_row)
        conn.commit()
        conn.close()
        
        #print("Data"+ str(data_row) +" Out Added!")

        return

    #This is peroid function update
    def update(period = 1000):

        global cap1,cap2,photo,photo1,face_locations_in,face_encodings_in,face_locations_out,face_encodings_out,name_in_prev,name_out_prev,name_in,name_out,dis_in,dis_out,Jennis

        check()#Check again folloe period

        ret1,frame1 = cap1.read()
        ret2,frame2 = cap2.read()
        frame_copy1 = frame1.copy()
        frame_copy2 = frame2.copy()

        #THREAD FACE IN 
        def process_in():  
            
            global face_locations_in,face_encodings_in
            
            # Get location and encoding this roi_face
            face_locations_in  = face_recognition.face_locations(frame1)
            face_encodings_in  = face_recognition.face_encodings(frame1,face_locations_in) 

        #THREAD FACE OUT 
        def process_out():  
            
            global face_locations_out,face_encodings_out
            
            # Get location and encoding this roi_face
            face_locations_out = face_recognition.face_locations(frame2)
            face_encodings_out = face_recognition.face_encodings(frame2,face_locations_out)       

        #Thread 2 flow
        #t1 = Thread(target = process_in)
        t1 = Thread(target = process_in,args = ())
        #t2 = Thread(target = process_out)
        t2 = Thread(target = process_out,args = ())
        t1.start()
        t2.start()
        t1.join() #Join every thing before Start to process next step
        t2.join() #Join every thing before Start to process next step

        #print("No face in: "  + str(len(face_locations_in)))
        #print("No face out: " + str(len(face_locations_out)))

        #IN PROCESS
        
        if (len(face_locations_in) != 0):

            try:
                for (top,right,bottom,left),face_encoding in zip(face_locations_in,face_encodings_in):
                    # See if face is a match for known faces
                    name = "Unknown_In"
                    # Compare known face encoding and unknown face encodning
                    matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
                    # Find the distance between these face
                    face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
                    # Return Best index match, the lowest
                    best_match_index = np.argmin(face_distances)
                    
                    # If matches at best_match_index is True anf face_distance lower than a accept_distance  
                    if matches[best_match_index] and face_distances[best_match_index] < accept_distance:
                        # Name = name of face
                        name = known_face_names[best_match_index] + " " + str(round(face_distances[best_match_index],2))
                        # Draw a rectangle
                        frame1 = cv2.rectangle(frame1,(left,top),(right,bottom),(0,255,0),2)
                        # Put the name in the text
                        frame1 = cv2.putText(frame1,name,(left,top-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),1)
                        # Crop and show the KNOWN FACE's window
                        roi_face1 = frame_copy1[top-thresh_y:bottom+thresh_y,left-thresh_x:right+thresh_x]
                        #cv2.imshow("Known_In",roi_face1)

                        # Do something after detect, add to dataframe,database, save image
                        t               = datetime.datetime.now()
                        time_now        = str(t)
                        date_clock      = time_now[0:10]
                        time_clock      = time_now[11:-1]                            # Add this into dataframe and Database
                        name            = known_face_names[best_match_index]         # Add this into dataframe and Database
                        name_in_prev    = name_in
                        name_in         = known_face_names[best_match_index]
                        typ             = "In"                                       # Add this into dataframe and Database
                        dis             = round(face_distances[best_match_index],2)  # Add this into dataframe and Database
                        dis_in          = dis
                        valin_prev.configure(text = name_in_prev)
                        valin_now.configure(text = name_in)
                        
                        if name_in_prev != name_in:
                            add_in()
                            # Save this image to face_known In
                            img_path = path_known + known_face_names[best_match_index] +"_In_"+ time_clock.replace(":","-") + ".jpg"
                            # Save your image
                            cv2.imwrite(img_path,roi_face1)

                            # Jennis and Arduino do something here
                            # Say hello here
                            say = "Hello " + known_face_names[best_match_index]
                            Jennis.say(say)
                            Jennis.runAndWait()
                    
                    else:
                        # Draw a rectangle
                        frame1 = cv2.rectangle(frame1,(left,top),(right,bottom),(0,255,0),2)
                        # Put the name in the text
                        frame1 = cv2.putText(frame1,name,(left,top-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),1)
                        # Crop and show the UNKNOWN FACE's window
                        roi_face1 = frame_copy1[top-thresh_y:bottom+thresh_y,left-thresh_x:right+thresh_x]
                        #cv2.imshow("Unknown_In",roi_face1)

                        # Do something after detect, add to dataframe,database, save image
                        t               = datetime.datetime.now()
                        time_now        = str(t)
                        date_clock      = time_now[0:10]
                        time_clock      = time_now[11:-1]
                        name            = "Unknown"
                        name_in_prev    = name_in
                        name_in         = "Unknown_In"
                        typ             = "In"   
                        dis             = round(face_distances[best_match_index],2)
                        dis_in          = dis
                        valin_prev.configure(text = name_in_prev)
                        valin_now.configure(text = name_in)
                        
                        if name_in_prev != name_in:
                            add_in()

                        # Save this image to face_Unknown
                        img_path = path_unknown + "Unknown_In_"+ time_clock.replace(":","-") + ".jpg"
                        # Save your image
                        cv2.imwrite(img_path,roi_face1)    

                        # Jennis and Arduino do something here
                        say = "You In, i don't know who you are, please Step closer!"
                        Jennis.say(say)
                        Jennis.runAndWait()

            except: pass
        
        else:

            name_in_prev = name_in
            name_in     = "No Face In"
            valin_prev.configure(text = name_in_prev)
            valin_now.configure(text = name_in)

        #OUT PROCESS 
        
        if (len(face_locations_out) != 0):

            try:
                for (top,right,bottom,left),face_encoding in zip(face_locations_out,face_encodings_out):
                    # See if face is a match for known faces
                    name = "Unknown_Out"
                    # Compare known face encoding and unknown face encodning
                    matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
                    # Find the distance between these face
                    face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
                    # Return Best index match, the lowest
                    best_match_index = np.argmin(face_distances)
                    
                    # If matches at best_match_index is True anf face_distance lower than a accept_distance
                    if matches[best_match_index] and face_distances[best_match_index] < accept_distance:
                        # Name = name of face
                        name = known_face_names[best_match_index] + " " + str(round(face_distances[best_match_index],2))
                        # Draw a rectangle
                        frame2 = cv2.rectangle(frame2,(left,top),(right,bottom),(0,255,0),2)
                        # Put the name in the text
                        frame2 = cv2.putText(frame2,name,(left,top-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),1)
                        # Crop and show the KNOWN FACE's window
                        roi_face2 = frame_copy2[top-thresh_y:bottom+thresh_y,left-thresh_x:right+thresh_x]
                        #cv2.imshow("Known_Out",roi_face2)

                        # Do something after detect, add to dataframe,database, save image
                        t                = datetime.datetime.now()
                        time_now         = str(t)
                        date_clock       = time_now[0:10]
                        time_clock       = time_now[11:-1]                    #Add this into dataframe and Database
                        name             = known_face_names[best_match_index]       #Add this into dataframe and Database
                        name_out_prev    = name_out
                        name_out         = known_face_names[best_match_index]
                        typ              = "Out"                                    #Add this into dataframe and Database
                        dis              = round(face_distances[best_match_index],2) #Add this into dataframe and Database
                        dis_out          = dis
                        valout_prev.configure(text = name_out_prev)
                        valout_now.configure(text = name_out)
                        
                        if name_out_prev != name_out:
                            add_out()
                            # Save this image to face_known Out
                            img_path = path_known + known_face_names[best_match_index] +"_Out_"+ time_clock.replace(":","-") + ".jpg"
                            #Save your image
                            cv2.imwrite(img_path,roi_face2)

                            # Jennis and Arduino do something here
                            # Say hello here
                            say = "Bye Bye" + known_face_names[best_match_index]
                            Jennis.say(say)
                            Jennis.runAndWait()
                    
                    else:
                        # Draw a rectangle
                        frame2 = cv2.rectangle(frame2,(left,top),(right,bottom),(0,255,0),2)
                        # Put the name in the text
                        frame2 = cv2.putText(frame2,name,(left,top-3),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),1)
                        # Crop and show the UNKNOWN FACE's window
                        roi_face2 = frame_copy2[top-thresh_y:bottom+thresh_y,left-thresh_x:right+thresh_x]
                        #cv2.imshow("Unknown_Out",roi_face2)

                        # Do something after detect, add to dataframe,database, save image
                        t                = datetime.datetime.now()
                        time_now         = str(t)
                        date_clock       = time_now[0:10]
                        time_clock       = time_now[11:-1]
                        name             = "Unknown"
                        name_out_prev    = name_out
                        name_out         = "Unknown"
                        typ              = "Out"   
                        dis              = round(face_distances[best_match_index],2)
                        dis_out          = dis
                        valout_prev.configure(text = name_out_prev)
                        valout_now.configure(text = name_out)
                        
                        if name_out_prev != name_out:
                            add_out()

                        # Save this image to face_Unknown
                        img_path = path_unknown + "Unknown_Out_"+ time_clock.replace(":","-") + ".jpg"
                        # Save your image
                        cv2.imwrite(img_path,roi_face2)

                        # Jennis and Arduino do something here
                        say = "You Out, i don't know who you are, please Step closer!"
                        Jennis.say(say)
                        Jennis.runAndWait()

            except: pass
        
        else:

            name_out_prev = name_out
            name_out     = "No Face Out"
            valout_prev.configure(text = name_out_prev)
            valout_now.configure(text = name_out)


        #Convert opencv numpy array into tkinter
        frame_inv1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
        frame_inv2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)
        photo  = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_inv1))
        photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_inv2))

        #Create canvas img
        my_canvas.create_image(7,20, image = photo, anchor =tk.NW)
        my_canvas.create_image(654,20, image = photo1, anchor =tk.NW)

        window_detect.after(period,update)

    #Check every time you open window detect, check ony once
    print(str(datetime.datetime.now()) + " CHECKING DATA...")

    check()

    #Update
    print(str(datetime.datetime.now()) + " DETECTING DATA...")
    
    update()

    window_detect.mainloop() #Loop your window if you dont do this, something go wrong, like your canvas

def func_analyst():
    #Label on home screen
    label_mode.config(text  = "Analyst Mode Activated")
    
################################################################################################################################################################################

# Create database
funct_datacreate()

################################################################################################################################################################################
#Create window_home screen, window size, logo,title
window_home = tk.Tk()
window_home.geometry("600x600")
window_home.title("Home Window")
window_home.iconbitmap(path_icon + "VVS_logo.ico")
window_home.resizable(width = False,height = False)
img_bg   = tk.PhotoImage(file = path_icon + "background1.png")
label_bg = tk.Label(window_home,image = img_bg)
label_bg.place(x = 0, y = 0,relwidth = 1, relheight = 1)

#Create element in window screen
#Create label in window screen
#Create label infom
label_panel = Label(window_home,text = "VVSAC Demo version" ,fg = "blue", font = ("Arial",30))
label_panel.grid(column = 0, row = 0,padx = 100, pady = 30) # Similar like pack

#Label for mode anoucement
label_mode = tk.Label(window_home,text = "")
label_mode.grid(column = 0,row = 4,padx = 10,pady = 10)

#Label for copy right
label_tail = tk.Label(window_home,text = "© 2021, Developed by VVSolutions_CHL, All for free! ")
label_tail.grid(column = 0,row = 5,padx = 10,pady = 10)

#Create button in window_home
#Collect button
icon_collect = tk.PhotoImage(file = path_icon + "image_collect.png")
button_collect = Button(window_home, image = icon_collect, borderwidth = 3, command = func_collect)
button_collect.grid(column = 0, row = 1, padx =10, pady = 10)

#Detect button
icon_detect = tk.PhotoImage(file = path_icon + "image_detect.png")
button_detect = Button(window_home, image = icon_detect, borderwidth = 3, command = func_detect)
button_detect.grid(column = 0, row = 2, padx = 10,pady = 10)

#Collect button
icon_analyst = tk.PhotoImage(file = path_icon + "image_analyst.png")
button_analyst = Button(window_home, image = icon_analyst, borderwidth = 3, command = func_analyst)
button_analyst.grid(column = 0,row = 3,padx = 10,pady = 10)

#window main loop
window_home.mainloop()
cap1.release()         # Release camera connection after press [X]
cap2.release()         # Release camera connection after press [X]