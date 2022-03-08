# import the necessary packages
import numpy as np
import cv2
import tkinter
import threading
import time
import tkinter.font as tkFont

# initialize the HOG descriptor/person detector

CounterMe=5

###Eingang
e1xmin=220
e1xmax=470

e1ymin=150
e1ymax=175

#Ausgang
e2xmin=10
e2xmax=620

e2ymin=250
e2ymax=290

#Abstand


###


###
class myFred(threading.Thread):
    def __init__(self, iD, name):
        threading.Thread.__init__(self)
        self.iD=iD
        self.name=name
    def run(self):
        Tk = tkinter.Tk()
        global message
        message = tkinter.StringVar()
        fontStyle = tkFont.Font(family="Lucida Grande", size=240)
        message.set("-1")
        label = tkinter.Label(Tk, textvariable=message, font=fontStyle).pack()
        Tk.mainloop()
        

    


t1=myFred(1,"t1")
t1.start()
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

# the output will be written to output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (720,480))

#Example (Hello, World):

PersonenListeBack=[[1,10,0,0],[1,0,0,0]]
PersonenListeFront=[[1,10,0,0],[1,0,0,0]]

while(True):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    print("F:"+str(PersonenListeFront))
    print("B:"+str(PersonenListeBack))
    
#
#
#
 

#Verschwunde Personen werden wenn Sie 10 Frames nicht gefunden werden gelöscht
#:#           
#Front +++++++++++++++++++++
    DEL=0 #DEL sind die gelöschten Einträge aus der LISTE 
    
    for c1 in range(0,len(PersonenListeFront)):
        if(PersonenListeFront[c1-DEL][0]==0):
            PersonenListeFront=np.delete(PersonenListeFront,(c1-DEL), axis=0)
            DEL+=1
        else:
            PersonenListeFront[c1-DEL][0]=PersonenListeFront[c1-DEL][0]-1          
#Back -------------------------  
    DEL=0 #DEL sind die gelöschten Einträge aus der LISTE 
    
    for c1 in range(0,len(PersonenListeBack)):
        if(PersonenListeBack[c1-DEL][0]==0):
            PersonenListeBack=np.delete(PersonenListeBack,(c1-DEL), axis=0)
            DEL+=1
        else:
            PersonenListeBack[c1-DEL][0]=PersonenListeBack[c1-DEL][0]-1
    DEL=0
#
#
#
    
#Eingangs und Ausgangs Zone werden makiert
#:#
#Eingang
    cv2.rectangle(frame, (e1xmin, e1ymin), (e1xmax, e1ymax),
                          (0, 255, 255), 2)
#Ausgang
    cv2.rectangle(frame, (e2xmin, e2ymin), (e2xmax, e2ymax),
                          (0, 255, 0), 2)
#
#
#
#Sperren löschen 
#:#
#Front +++++++++++++++++++++
    for listnr in range(0, len(PersonenListeFront)):
        PersonenListeFront[listnr][3]=0

#Back +++++++++++++++++++++
    for listnr in range(0, len(PersonenListeBack)):
        PersonenListeBack[listnr][3]=0
        
        
    for (xA, yA, xB, yB) in boxes:
    
        #malen der BOX
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 0, 255), 2)
        ly=yA+((yB-yA)/2)
        lx=xA+((xB-xA)/2)
        
        
        print(str(lx)+":"+str(ly))   


#frame malen für den Mittelpunkt der Person        
        for ix in range(-2, 3):
                for iy in range(-2, 3):
                    frame[int(ly+iy),int(lx+ix)]=[0,0,255]
        
   
#Forward 
        fk=0 #Frontk
        for listnr in range(0, len(PersonenListeFront)):
            difflx=PersonenListeFront[listnr-DEL][1]-lx
            diffly=PersonenListeFront[listnr-DEL][2]-ly
            print("difflx:"+str(difflx)+"    "+"diffly:"+str(diffly))
            if(difflx>-40 and difflx<40 and diffly>-40 and diffly<40 and PersonenListeFront[listnr-DEL][3]!=1):
                fk=1 # Eine vorhandene Person wurde gefunden
                PersonenListeFront[listnr-DEL][1]=lx
                PersonenListeFront[listnr-DEL][2]=ly
                PersonenListeFront[listnr-DEL][0]=10
                PersonenListeFront[listnr-DEL][3]=1
                for ix in range(-2, 3):
                    for iy in range(-2, 3):
                        frame[int(ly+iy),int(lx+ix)]=[0,255,255]
                
                if(lx>e2xmin and lx<e2xmax and ly>e2ymin and ly<e2ymax):
                    CounterMe+=1
                    datei = open('textdatei.txt','w')
                    datei.write(str(CounterMe))   
                    datei.close()                      
                    PersonenListeFront=np.delete(PersonenListeFront,(listnr-DEL), axis=0)
                    DEL+=1               
                break
                
        if(fk==0):
            if(lx>e1xmin and lx<e1xmax and ly>e1ymin and ly<e1ymax):
                PersonenListeFront=np.append(PersonenListeFront,[[5,int(lx),int(ly),0]], axis=0)
             
#Back    
        bk=0  # Back k  
        for listnr in range(0, len(PersonenListeBack)):
            difflx=PersonenListeBack[listnr-DEL][1]-lx
            diffly=PersonenListeBack[listnr-DEL][2]-ly
            print("difflx:"+str(difflx)+"    "+"diffly:"+str(diffly))
            if(difflx>-40 and difflx<40 and diffly>-40 and diffly<40 and PersonenListeBack[listnr-DEL][3]!=1):
                bk=1 # Eine vorhandene Person wurde gefunden
                PersonenListeBack[listnr-DEL][1]=lx
                PersonenListeBack[listnr-DEL][2]=ly
                PersonenListeBack[listnr-DEL][0]=10
                PersonenListeBack[listnr-DEL][3]=1
                for ix in range(-2, 3):
                    for iy in range(-2, 3):
                        frame[int(ly+iy),int(lx+ix)]=[0,255,0]
                
                if(lx>e1xmin and lx<e1xmax and ly>e1ymin and ly<e1ymax):
                    CounterMe-=1
                    datei = open('textdatei.txt','w')
                    datei.write(str(CounterMe))
                    datei.close()                    
                    PersonenListeBack=np.delete(PersonenListeBack,(listnr-DEL), axis=0)
                    DEL+=1               
                break
                
        if(bk==0):
            if(lx>e2xmin and lx<e2xmax and ly>e2ymin and ly<e2ymax):
                PersonenListeBack=np.append(PersonenListeBack,[[5,int(lx),int(ly),0]], axis=0)
                                
    
    # Write the output video
    message.set(CounterMe)
    out.write(frame.astype('uint8'))
    # Display the resulting frame
    print("############################")
    cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("frame",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)  