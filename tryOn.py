from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2, threading, os, time
from threading import Thread
from os import listdir
from os.path import isfile, join

import dlib
from imutils import face_utils, rotate_bound
import math


def put_sprite(num):
    global SPRITES, BTNS
    SPRITES[num] = (1 - SPRITES[num]) 
    # if SPRITES[num]:
    #     BTNS[num].config(relief=SUNKEN)
    # else:
    #     BTNS[num].config(relief=RAISED)

def draw_sprite(frame, sprite, x_offset, y_offset):
    (h,w) = (sprite.shape[0], sprite.shape[1])
    (imgH,imgW) = (frame.shape[0], frame.shape[1])

    if y_offset+h >= imgH:
        sprite = sprite[0:imgH-y_offset,:,:]

    if x_offset+w >= imgW:
        sprite = sprite[:,0:imgW-x_offset,:]

    if x_offset < 0: 
        sprite = sprite[:,abs(x_offset)::,:]
        w = sprite.shape[1]
        x_offset = 0

    for c in range(3):
            #print(c)
            frame[y_offset:y_offset+h, x_offset:x_offset+w, c] =  \
            sprite[:,:,c] * (sprite[:,:,3]/255.0) +  frame[y_offset:y_offset+h, x_offset:x_offset+w, c] * (1.0 - sprite[:,:,3]/255.0)
    return frame

def adjust_sprite2head(sprite, head_width, head_ypos, ontop = True):
    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
    #print("heigth")
    #print(h_sprite )
    #print("ori w is " , w_sprite)
    #w_sprite = w_sprite *2
    #print("increase w is " , w_sprite)
    #factor = 1.25*head_width/w_sprite  this one
    #factor = (1.0*head_width/w_sprite)
    factor = head_width/ w_sprite
    sprite = cv2.resize(sprite, (0,0), fx=factor, fy=factor)
    (h_sprite,w_sprite) = (sprite.shape[0], sprite.shape[1])
    y_orig = head_ypos

    # """ y_orig =  head_ypos-h_sprite if ontop else head_ypos 
    # if (y_orig < 0):
    #         sprite = sprite[abs(y_orig)::,:,:] 
    #         y_orig = 0 """
    return (sprite, y_orig)


def apply_sprite(image, path2sprite,w,x,y, angle, ontop = True):
    sprite = cv2.imread(path2sprite,-1)
    #sprite = rotate_bound(sprite, angle)
    (sprite, y_final) = adjust_sprite2head(sprite, w, y, ontop)
    #y_final = y
            #x= x-10
    #x = x-int(0.31*x)
    #x = x-int((10/13)*x)
    #x = x-int((10/13)*w)
    #x = x - int((0.125) *w) This one
    y_final = y_final - int((w/2)/4)
    image = draw_sprite(image,sprite,x, y_final)

def calculate_inclination(point1, point2):
    x1,x2,y1,y2 = point1[0], point2[0], point1[1], point2[1]
    incl = 180/math.pi*math.atan((float(y2-y1))/(x2-x1))
    return incl


def calculate_boundbox(list_coordinates):
    x = min(list_coordinates[:,0])
    y = min(list_coordinates[:,1])
    w = max(list_coordinates[:,0]) - x
    h = max(list_coordinates[:,1]) - y
    return (x,y,w,h)


def get_face_boundbox(points, face_part):
    if face_part == 1:
        (x,y,w,h) = calculate_boundbox(points[17:22]) #right eyebrow
    elif face_part == 2:
        (x,y,w,h) = calculate_boundbox(points[22:27]) #left eyebrow
    elif face_part == 3:
        (x,y,w,h) = calculate_boundbox(points[36:42]) #right eye
    elif face_part == 4:
        (x,y,w,h) = calculate_boundbox(points[42:48]) #left eye
    elif face_part == 5:
        (x,y,w,h) = calculate_boundbox(points[29:36]) #nose(but it should 27)
    elif face_part == 6:
        (x,y,w,h) = calculate_boundbox(points[0:17]) #jaw
    elif face_part == 7:
        # (x,y,w,h) = calculate_boundbox(points[48:68]) #mouth
        (x,y,w,h) = calculate_boundbox(points[1:5]) #maybe right cheek
    elif face_part == 8:
        (x,y,w,h) = calculate_boundbox(points[12:16]) #maybe left cheek
    return (x,y,w,h)

image_path = ''
video_capture = ''
def add_sprite(img):
    global image_path
    image_path = img
    print(img.rsplit('/',1))
    print("in sprite")
    print(int(img.rsplit('/',1)[0][-1]))
    put_sprite(int(img.rsplit('/',1)[0][-1]))
    
#Principal Loop where openCV (magic) occurs
def cvloop(run_event):
    global panelA
    global SPRITES
    global image_path
    global video_capture
    i = 0
    video_capture = cv2.VideoCapture(0) #read from webcam
    # print("FPS1 is ")
    # print(cv2.CAP_PROP_FPS)
    (x,y,w,h) = (0,0,10,10) #whatever initial values
    facePath = "F://University Student Lay/6th year/Thesis/Code/Virtual Try On System/data/haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(facePath)
    

    #Filters path
    #detector = dlib.get_frontal_face_detector()

    #model = "data/shape_predictor_68_face_landmarks.dat"
    #predictor = dlib.shape_predictor(model) # link to model: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

    while run_event.is_set(): 
        ret, image = video_capture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # the whole captured image(frame)
        #faces = detector(gray, 0)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # print("FPS is ")
        # print(cv2.CAP_PROP_FPS) # frame per second printing

        for face in faces: 
            (x,y,w,h) = (face[0], face[1], face[2], face[3])
            #nh = int(1/8 * h)
            nnh = int(1/6*h)
            y = y-nnh
            cv2.rectangle(image, (x, y), (x+w, y+h+nnh), (255, 0, 0), 2)
            
            # necklace and it is correct, but i change it for top
            if SPRITES[1]:
                #(x1,y1,w1,h1) = get_face_boundbox(shape, 6)
                #apply_sprite(image,image_path,w1,x1,y1+275, incl)
                cv2.rectangle(image, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)
                wn = int(1.4 * w1)
                yn = int (y1+(6.5*h1))
                apply_sprite(image,image_path,3.5*w1,x1-wn,yn, 0)
            
             # clone from above and lote chin yar lote yan for top
             # at first i take the jaws points , x1,y1,w1,h1 , but now is with face points
            if SPRITES[0]:
                #(x1,y1,w1,h1) = get_face_boundbox(shape, 6)
                #w1 = int(w1*1.5)
                #apply_sprite(image,image_path,w1,x1,y1+275, incl)
                #h1 = h +nnh
                h = h  + nnh + 38
                #h = h+ nnh +nnh
                #y = y-(2*nnh)
                xCent = x+ (0.5 * w)
                #xSh = xCent - (2*h)
                xSh = xCent - h
                #ySh = y1 + ((1.5)*h1)
                #ySh = y+(h1*(4/3)) -nnh
                ySh = y+(h*(4/3)) -38
                xSh = int(xSh)
                ySh = int(ySh)
                #cv2.rectangle(image, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)
                #wn = int(2* (xCent - xSh))
                wn = int(2*h)
                hn = 6*h
                cv2.rectangle(image, (xSh, ySh), (xSh+wn, ySh+hn), (0, 0, 255), 2)
                apply_sprite(image,image_path,wn,xSh,ySh, 0)

            

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panelA.configure(image=image)
        panelA.image = image
    video_capture.release()

# Initialize GUI object
root = Tk()
root.title("Virtual Try On")
# os.path.realpath(__file__) = F:\University Student Lay\6th year\Thesis\Code\Virtual Try On System\tryOn.py
# os.path.dirname(os.path.realpath(__file__)) = F:\University Student Lay\6th year\Thesis\Code\Virtual Try On System
this_dir = os.path.dirname(os.path.realpath(__file__))
btn1 = None

def try_on(image_path):
    btn1 = Button(root, text="Try It On!", command = lambda:add_sprite(image_path))
    btn1.pack(side="top", fill="both", expand="no", padx="5", pady="5")
    

panelA = Label(root)
panelA.pack( padx=10, pady=10)

SPRITES = [0,0,0,0,0,0,0]
BTNS = [btn1]
#print(sys.argv[1]) >> sys.argv[1] = static/images/Tops4/3.png
try_on(sys.argv[1])

run_event = threading.Event()  # returns a new event object
run_event.set()  # set flag to true
action = Thread(target=cvloop, args=(run_event,))
action.setDaemon(True)
action.start()   # call to cvloop

def terminate():
        global root, run_event, action,video_capture
        print(run_event.is_set())
        run_event.clear()  # set thread flag to false
        print(run_event.is_set())
        time.sleep(1)
        video_capture.release()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", terminate)
root.mainloop() 