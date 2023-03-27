import cv2 as cv 
import glob 

def testDevice(source):
   cap = cv.VideoCapture(source) 
   if cap is None or not cap.isOpened():
       print('Warning: unable to open video source: ', source)
       return
   else:
       print("Worked on : ",source)
for camera in glob.glob("/dev/video?"):
	testDevice(camera) # no printout
