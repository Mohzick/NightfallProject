import sys
import argparse
import os
import shutil

import crop
import videowrap

import cv2
print(cv2.__version__)

import time
start = time.time()

counter = 0

parser = argparse.ArgumentParser()
parser.add_argument("--inFolder", help="Input videos folder")
parser.add_argument("--outFolder", help="Empty output folder")
args = parser.parse_args()

#for arg in vars(args):
    #print('[{0}] = '.format(arg),  getattr(args, arg))


'''
  extractImages takes a file path and an output folder path
  extracts 1/2 frames of the video into the output folder
'''
def extractImages(inFile, outFolder):

    global counter
    completionCounter = 0

    vidcap = cv2.VideoCapture(inFile)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    success = True #why

    while success:

      success,image = vidcap.read()
      counter += 1
      completionCounter += 1
      if success:
        if counter%2 == 0:
          imgName = str(counter).zfill(6)

          cv2.imwrite( outFolder + "/" + imgName + ".jpg", image)     # save frame as JPEG file
          percentage = int((completionCounter/length)*100)
          print("Progress = {0} %...".format(percentage), end='\r')


if __name__=="__main__":

    tempOutput = "tempOutput"

    if not os.path.isdir(tempOutput):
        os.makedirs(tempOutput)

    print("\n------------\nThank you for choosing our extracting and cropping program.\n------------\n")
    for entry in os.scandir(args.inFolder):
        if entry.is_file():
            print("\n------------\nBeginning work on video {0}: extracting 1/2 frames and storing them into {1}.\n------------\n".format(entry.path, args.outFolder))
            extractImages(entry.path, tempOutput)
            print("\n------------\nWork on video {0} is complete!\n------------\n".format(entry.path))

    if not os.path.isdir(args.outFolder):
        os.makedirs(args.outFolder)

    print("\n------------\nSuccessfully extracted images from videos in {0}.".format(args.inFolder))
    print("Now attempting to crop each image, storing them into {0}.\n------------\n\n".format(args.outFolder))

    crop.cropper(350, 1, 850, tempOutput, args.outFolder)

    shutil.rmtree(tempOutput)

    print("\n\n------------\nSuccessfully extracted and cropped every images from the {0} folder.\n------------\n\n".format(args.inFolder))

    print("Now attempting to convert the images into a mp4 video.\n------------\n\n\n")

    videowrap.folderToVideo(args.outFolder, "outVideoTest.mp4")

    print("\nconversion complete.\n\n\n")

end = time.time()
totalTime = end - start
print("Process time:", totalTime, "seconds.")