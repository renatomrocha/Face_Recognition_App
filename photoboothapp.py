from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os




class PhotoBoothApp:
    def __init__(self, vs):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
            
            self.vs = vs
	    #self.outputPath = outputPath
            self.frame = None
            self.thread = None
            self.act = False
            
            self.stopEvent = None
            
            
		# initialize the root window and image panel
            self.root = tki.Tk()

            self.panel = None


            self.rec = tki.IntVar()        
            self.rec.set(1)

            btn = tki.Button(self.root, text="Detect",
			command=self.Snap_thread)

            btn.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)
            btn1 = tki.Button(self.root, text="Stop!",
			command=self.stop)

            btn1.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)
            rbtn1 = tki.Radiobutton(self.root, text = "Face", justify = tki.LEFT, variable = self.rec, value=1)


            rbtn1.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)

            rbtn2 = tki.Radiobutton(self.root, text = "Eyes", justify = tki.RIGHT, variable = self.rec, value=2)


            rbtn2.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)


            rbtn3 = tki.Radiobutton(self.root, text = "Smile", justify = tki.RIGHT, variable = self.rec, value=3)

            rbtn3.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)

            rbtn4 = tki.Radiobutton(self.root, text = "Eyes and Face", justify = tki.RIGHT, variable = self.rec, value=4)

            rbtn4.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)

            
		# start a thread that constantly pools the video sensor for
		# the most recently read frame
            self.stopEvent = threading.Event()
            self.thread = threading.Thread(target=self.videoLoop, args=())
            self.thread.start()
 
		# set a callback to handle when the window is closed
            self.root.wm_title("PyImageSearch PhotoBooth")
            self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
            
    def Snap_thread(self):
        
        self.ti = threading.Thread(target = self.takeSnapshot)
        self.ti.start()


    def videoLoop(self):
        self.ret, self.frame = self.vs.read()
        self.man_img = self.frame

        try:

            while not self.stopEvent.is_set():


                self.ret, self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                #self.img = self.frame
                 

                if(self.act == True):
                    
                    image = self.man_img
                    image = imutils.resize(image, width=300)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image)

                else:
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image)
                    
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError:
            print("[INFO] caught a RuntimeError")


            
    def takeSnapshot(self):
        print("Processing data...")
        print("Val: ", self.rec.get())
        
        self.act = True
        
        while (self.act==True):
            
            
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
            
            img = self.frame

            #FACE Detection
            if(self.rec.get()==1):
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.putText(img,'Face',(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1 ,(255,0,0),2,cv2.LINE_AA)
                    roi_gray = gray[y:y+h, x:x+w]
                
                
                    roi_color = img[y:y+h, x:x+w]
                    #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
                    #eyes = eye_cascade.detectMultiScale(roi_gray)
                    #for (ex,ey,ew,eh) in eyes:
                        #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            #EYES DETECTION
            elif(self.rec.get()==2):
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
                for (x,y,w,h) in faces:
                    #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                
                
                    roi_color = img[y:y+h, x:x+w]
                    eye_cascade = cv2.CascadeClassifier('frontalEyes35x16.xml')
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


            #SMILE DETECTION
            elif(self.rec.get()==3):
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
                for (x,y,w,h) in faces:
                    #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                
                
                    roi_color = img[y:y+h, x:x+w]
                    smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
                    smile = smile_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in smile:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                        #cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)

            elif(self.rec.get()==4):
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                
                
                    roi_color = img[y:y+h, x:x+w]
                    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


                    
            self.man_img = img
            
        print("Stopped Processing")      
            

    def stop(self):
        self.act = False
        
        
    def onClose(self):

        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.release()
        
        self.root.quit()
        
        
    

