import sys
import argparse
import os

import cv2
print(cv2.__version__)

counter = 0

parser = argparse.ArgumentParser()
parser.add_argument("--inFolder", help="Input videos folder")
parser.add_argument("--outFolder", help="Empty output folder")
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg,  getattr(args, arg))

def extractImages(inFolder, outFolder):

    global counter

    vidcap = cv2.VideoCapture(inFolder)
    #success,image = vidcap.read()

    success = True #why

    while success:

      success,image = vidcap.read()
      print(success)
      counter += 1
      if success:
        if counter%2 == 0:
          cv2.imwrite( outFolder + "\\frame%d.jpg" % counter, image)     # save frame as JPEG file

if __name__=="__main__":
     
    for entry in os.scandir(args.inFolder):
        if entry.is_file():
            #files.append(entry.path)
            extractImages(entry.path, args.outFolder)
  

