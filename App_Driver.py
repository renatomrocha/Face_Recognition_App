from __future__ import print_function
from photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time
import cv2
import os

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-o", "--output", required=True,
#	help="path to output directory to store snapshots")
#ap.add_argument("-p", "--picamera", type=int, default=-1,
#	help="whether or not the Raspberry Pi camera should be used")
#args = vars(ap.parse_args())
 
# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = cv2.VideoCapture(0)
time.sleep(2.0)
 
# start the app
pba = PhotoBoothApp(vs)
pba.root.mainloop()


