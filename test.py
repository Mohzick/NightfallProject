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

import cv2

import time
size = 352

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--type", help="webcam, video or testing folder?")
parser.add_argument("--model", help="model to test with")
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

end = time.time()
totalTime = end - start
print("Process time:", totalTime, "seconds")

