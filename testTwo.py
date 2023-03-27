import cv2, glob

for camera in glob.glob("/dev/video?"):
	c = cv2.VideoCapture(camera)
