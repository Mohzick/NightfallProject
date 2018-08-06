from __future__ import print_function
import argparse
import os
from math import log10
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
import torchvision.transforms as transforms

from imagesDataset import saveImage
from PIL import Image
from gan import createGenerator, createDiscriminator, GANLoss, print_net
from imagesDataset import getTrainingDataset, getTestingDataset
import torch.backends.cudnn as cudnn
import interface
import argparse

import dataset.frame as frame
import dataset.crop as crop
import dataset.videowrap as videowrap

import cv2

import time
import shutil
size = 352
outvideo = "Results/video"
realoutvideo = outvideo + "/test"

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--type", help="webcam, video or testing folder?")
parser.add_argument("--model", help="model to test with")
parser.add_argument("--videopath", help="video path", default = "None")
args = parser.parse_args()

model = "models/" + args.model
gen = torch.load(model)

print('------ MODEL LOADED ------')

if (args.type == "webcam"):
	print('---------------- INITIALIZING WEBCAM WINDOW ----------------------')
	interface.init_app()
	interface.init_window(x=320, w=(interface.screen_size().width()-320), h=(interface.screen_size().width()-320)*0.4)
	boucle = True
	capture = cv2.VideoCapture(0)
	transformation = transforms.Compose([transforms.ToTensor(), 
                                                 transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]) 
	while(boucle):
		ok, img = capture.read()
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		img = Image.fromarray(img)
		img = img.convert('RGB')
		img = img.resize((size, size), Image.BICUBIC)

		img2 = transformation(img)
		img2.unsqueeze_(0)
		if(torch.cuda.is_available()):
			img2 = img2.cuda()
		
		#print(type(img))
		#cv2.imshow('frere', img)
		#cv2.waitKey(0)
		#img2 = img.asarray(img)
		#img2 = img2.transforms.Compose([transforms.ToTensor(), 
	                                  #transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
		
		img3 = gen(img2)
		img3 = img3.detach().data[0]
		image_numpy = img3.cpu().float().numpy()
		'''print(type(image_numpy))
		print(image_numpy.shape)'''
		image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
		image_numpy = image_numpy.astype(np.uint8)
		image_pred = Image.fromarray(image_numpy)
		imgin = np.array(img)
		imgout = np.array(image_pred)
		interface.update_image(0, imgin)
		interface.update_image(1, imgout)
		interface.process_events()

if (args.type == "video"):
	if (args.videopath == "None"):
		print("You should input the video path as an argument")
	else:
		video = args.videopath
		tempOutput = "tempOutput"
	
	if not os.path.isdir(tempOutput):
		os.makedirs(tempOutput)

	print("\n------------\nThank you for choosing our extracting and cropping program.\n------------\n")
	print("\n------------\nBeginning work on video {0}: extracting video frames and storing them into {1}.\n------------\n".format(video, outvideo))
	frame.extractImages(video, tempOutput)
	print("\n------------\nWork on video {0} is complete!\n------------\n".format(video))
	print("\n------------\nSuccessfully extracted images from videos in {0}.".format(video))
	print("Now attempting to crop each image, storing them into {0}.\n------------\n\n".format(outvideo))
	crop.cropper(size, 1, 850, tempOutput, outvideo)
	shutil.rmtree(tempOutput)
	print("\n\n------------\nSuccessfully extracted and cropped every images from the {0} folder.\n------------\n\n".format(video))
	print("Networks processing.\n------------\n\n\n")
	testing_set = getTestingDataset(outvideo)
	testing_data_loader = DataLoader(dataset = testing_set, num_workers = 0, batch_size = 1, shuffle = False)
	real_Night = torch.FloatTensor(1, 3, size, size)
	real_Night = Variable(real_Night)
	if (torch.cuda.is_available()):
		real_Night = real_Night.cuda()
		gen = gen.cuda()
	print(testing_set.__len__())

	for iteration, batch in enumerate(testing_data_loader, 1):

		real_Night_cpu = batch[0]
		real_Night.data.resize_(real_Night_cpu.size()).copy_(real_Night_cpu)
		real_Night.unsqueeze_(0)
		fake_Day = gen(real_Night)
		data = fake_Day.detach().data[0]
		string1 = outvideo + "/test/image"
		string12 = "%d" % iteration
		stringExtension = ".jpg"
		string14 = string1 + string12 + stringExtension
		saveImage(data.cpu(), string14)

	print("Now attempting to convert the images into a mp4 video.\n------------\n\n\n")

	videowrap.folderToVideo(realoutvideo, "outVideoTest.mp4")
	print("\nconversion complete.\n\n\n")


end = time.time()
totalTime = end - start
print("Process time:", totalTime, "seconds")

