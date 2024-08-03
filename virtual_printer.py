# Importing modules
import cv2
import mediapipe as mp
import hand_tracking_module as htm
import os
import numpy as np

folder_path='E:\Desktop\MACHINE LEARNING\Computer Vision\Advanced\Hand Tracking\images'
images=os.listdir(folder_path)

# Reading the Images
read_images=[]
for image in images:
    img=cv2.imread(f'{folder_path}/{image}')
    read_images.append(img)
blue=read_images[0] # For the selection of blue colour pop up
eraser=read_images[1] # For the selection of eraser pop up
green=read_images[2] # For the selection of green colour pop up
header=read_images[3] # For the selection of header pop up
red=read_images[4] # For the selection of red colour pop up

draw_colour=(0,0,255)
thickness=15
eraser_thickness=50
xp,yp=0,0
img_canvas=np.zeros((720,1280,3),np.uint8) # It will return a black screen

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.HandDetetor(detection_conf=0.8)

while cap.isOpened():
    success,frame=cap.read()
    frame=cv2.flip(frame,1)
    
    frame=detector.hands_detection(frame) # Detecting Hands
    landmarks=detector.hand_landmark(frame,0) # Landmarks Detection
    
    ## For selecting the above options when the webcam will open
    if len(landmarks)!=0:
        x8,y8=landmarks[8][1],landmarks[8][2] # Cordinates of the tip of index finger
        x12,y12=landmarks[12][1],landmarks[12][2] # Cordinates of the tip of middle finger
        x16,y16=landmarks[16][1],landmarks[16][2] # Cordinates of the tip of ring finger
        
        if y12<=y8 or y16<=y8:
            print('Selection mode')
            if y8<125:
                xp,yp=0,0
                if 125< x8 <300:
                    header=red
                    draw_colour=(0,0,255)
                elif 350< x8 <525:
                    header=green
                    draw_colour=(0,255,0)
                elif 575< x8 <725:
                    header=blue
                    draw_colour=(255,0,0)
                elif 800< x8 <1100:
                    header=eraser
                    draw_colour=(0,0,0)
            else:
                header=header
            ## Drawing a rectangle between the cordinates of the tip of middle and index finger
            cv2.rectangle(frame,(x8,y8-20),(x12,y12+20),
                          draw_colour,cv2.FILLED)

        ## For drawing the selected color when the webcam will opened
        elif y8<y12 and y8<y16:
            ## Drawing a circle on the tip of index finger
            cv2.circle(frame,(x8,y8),8,
                       draw_colour,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x8,y8

            if draw_colour==(0,0,0):
                cv2.line(frame,(xp,yp),(x8,y8),draw_colour,eraser_thickness)
                cv2.line(img_canvas,(xp,yp),(x8,y8),draw_colour,eraser_thickness)
            else:
                cv2.line(frame,(xp,yp),(x8,y8),draw_colour,thickness)
                cv2.line(img_canvas,(xp,yp),(x8,y8),draw_colour,thickness)
            xp,yp=x8,y8
            print('Drawing mode')

    img_gray=cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY) # Converting the black screen into gray image
    _,img_inv=cv2.threshold(img_gray,50,255,cv2.THRESH_BINARY_INV) # Inverting the color of black screen (i.e white screen)
    img_inv=cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR) # Converting the white screen to BGR
    
    frame=cv2.bitwise_and(frame,img_inv) # Merging the white screen to webcam 
    frame=cv2.bitwise_or(frame,img_canvas) # Merging the black screen to webcam

    frame[0:125,0:1280]=header # Setting header image

    cv2.imshow('Virtual Painting',frame)
    # cv2.imshow('canvas',img_inv)
    
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
