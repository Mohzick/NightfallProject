import cv2
import os
import argparse

def folderToVideo(inFolder, outVideo):

	ext = "jpg"

	images = []
	for f in sorted(os.listdir(inFolder)):
	    if f.endswith(ext):
	        images.append(f)

	# Determine the width and height from the first image
	image_path = os.path.join(inFolder, images[0])
	frame = cv2.imread(image_path)
	cv2.imshow('video',frame)
	height, width, channels = frame.shape

	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
	out = cv2.VideoWriter(outVideo, fourcc, 15.0, (height, width))



	for image in images:

	    image_path = os.path.join(inFolder, image)
	    frame = cv2.imread(image_path)

	    out.write(frame) # Write out frame to video

	    cv2.imshow('video',frame)

	# Release everything if job is finished
	out.release()

	print("The output video is {}".format(outVideo))
