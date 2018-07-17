import cv2
import os
import argparse

def folderToVideo(inFolder, outVideo):

	# Arguments
	#inFolder = 'C:\\Users\\minh-ng\\Documents\\GitHub\\NightfallProject2\\dataset\\SingleImages\\DN1\\Day'
	ext = "jpg"
	#outVideo = "salut.mp4"

	images = []
	for f in os.listdir(inFolder):
	    if f.endswith(ext):
	        images.append(f)

	# Determine the width and height from the first image
	image_path = os.path.join(inFolder, images[0])
	frame = cv2.imread(image_path)
	cv2.imshow('video',frame)
	height, width, channels = frame.shape

	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
	out = cv2.VideoWriter(outVideo, fourcc, 15.0, (width, height))



	for image in images:

	    image_path = os.path.join(inFolder, image)
	    frame = cv2.imread(image_path)

	    out.write(frame) # Write out frame to video

	    cv2.imshow('video',frame)
	    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
	        break

	# Release everything if job is finished
	out.release()
	#cv2.destroyAllWindows()

	print("The output video is {}".format(outVideo))
	#does not work on linux: https://github.com/ContinuumIO/anaconda-issues/issues/223
