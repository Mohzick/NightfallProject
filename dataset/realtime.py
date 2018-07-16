import numpy as np
import cv2
import time
import sys, getopt
 
from video import create_capture
from common import clock, draw_str
 
args, video_src = getopt.getopt(sys.argv[1:], '', 'shotdir=')
args = dict(args)
shotdir = args.get('--shotdir', '.')

try:
    video_src = video_src[0]
except:
    video_src = 0
shot_idx = 0
 
cam = create_capture(video_src)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 350)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 350)
 
while True:
    ret, img = cam.read()
    imgs = []
    vis = img.copy()
    imgs.append(img)
    cv2.imshow('Video', vis)

cv2.destroyAllWindows()