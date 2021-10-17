from time import time
import cv2,pandas
from datetime import datetime

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0,cv2.CAP_DSHOW)  # to solve a bug in MSMF backend of opencv, need to add "cv2.CAP_DSHOW"

while True:
    check, frame = video.read()             # create frame object which will read images of video
    status=0

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame=gray        # get first frame of video
        continue
    
    delta_frame=cv2.absdiff(first_frame,gray)      # get difference between first frame and gray scale image

# To classify values of delta frame, need to assign threshold. 
# If difference is more than 30, assign white color to the pixel and less than 30 assign black color

    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]   

# dilate to smooth an image. Iteration specifies that how many time you want to go through an image to remove holes.
# Iterations directly propertional to smoothness of an image
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)   

# Now need to find Contours (Contours are defined as the line joining all the points along the boundary of an image that are having the same intensity.) of dilated threshold frame.
# There are 2 methods for Contour detection with openCV
# 1.Find contours = Find contours in an image and store them in a tuple 
# 2.Draw contours = Draws contours in an image   
# Here in this case, we want to find the contours and check if the area of this contour. So find contours and store them in a tuple
# Retrieve extrernal method to draw external contours. Approximation method for retrieving contours 

    (cnts,_) =cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue   
        status=1                         # if contourArea of contour is less than 1000 then go to the next contour
    
        (x,y,w,h)=cv2.boundingRect(contour)     # we will get values for a rectangle 
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    status_list.append(status)

    status_list=status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Capturing",gray)
    cv2.imshow("delta frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color frame",frame)

    key=cv2.waitKey(1)

    if key==ord('q'):                   # Use keyword "q" to quit
        if status==1:
            times.append(datetime.now())
        break
    
print(times)
print(status_list)

for i in range(0,len(times),2):                                                # To get data everytime when some object comes into the picture
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows