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

import cv2

import time
start = time.time()

input_rgb = 3
output_rgb = 3
gen_filters = 64
dis_filters = 64
threads = 0
batchSize = 1
batchSizeT = 1
lr = 0.0002
beta1 = 0.5
lamb = 10
nbEpochs = 1

size = 352
torch.cuda.manual_seed(123)
print('------------------------ DATASET LOADING ------------------------')

main_path = "DatasetInput/"

training_set = getTrainingDataset(main_path)
testing_set = getTestingDataset(main_path)

training_data_loader = DataLoader(dataset = training_set, num_workers = threads, batch_size = batchSize, shuffle = True)
testing_data_loader = DataLoader(dataset = testing_set, num_workers = threads, batch_size = batchSizeT, shuffle = False)

print('------------------------ DATASET LOADED ------------------------')

print('------------------------ BUILDING GAN ------------------------')

#gen = createGenerator(input_rgb, output_rgb, gen_filters, 'batch', [0])
#dis = createDiscriminator(input_rgb + output_rgb, dis_filters, 'batch', [0])
gen = torch.load("genmodel.pth")
dis = torch.load("dismodel.pth")

criterionGAN = GANLoss()
criterionL1 = nn.L1Loss()
criterionMSE = nn.MSELoss()

optimizerGen = optim.Adam(gen.parameters(), lr = lr, betas = (beta1, 0.999))
optimizerDis = optim.Adam(dis.parameters(), lr = lr, betas = (beta1, 0.999))

print('------------------------ GAN BUILT ------------------------')

print_net(gen)
print_net(dis)

print('------------------------ ------------------------ ------------------------')

real_Night = torch.FloatTensor(batchSize, input_rgb, size, size)
real_Day = torch.FloatTensor(batchSize, input_rgb, size, size)

real_Night = Variable(real_Night)
real_Day = Variable(real_Day)

if torch.cuda.is_available():
	gen = gen.cuda()
	dis = dis.cuda()
	criterionGAN = criterionGAN.cuda()
	criterionL1 = criterionL1.cuda()
	criterionMSE = criterionMSE.cuda()
	real_Night = real_Night.cuda()
	real_Day = real_Day.cuda()


def train(epoch):

	for iteration, batch in enumerate(training_data_loader, 1):

		real_Night_cpu, real_Day_cpu = batch[0], batch[1]
		real_Night.data.resize_(real_Night_cpu.size()).copy_(real_Night_cpu)
		real_Day.data.resize_(real_Day_cpu.size()).copy_(real_Day_cpu)

		fake_Day = gen(real_Night)


		#Train the Discriminator

		optimizerDis.zero_grad()

		#with fake
		fake_DayNight = torch.cat((real_Night, fake_Day), 1)
		pred_fake = dis.forward(fake_DayNight.detach())
		loss_d_fake = criterionGAN(pred_fake, False)

		#with real
		real_DayNight = torch.cat((real_Night, real_Day), 1)
		pred_real = dis.forward(real_DayNight)
		loss_d_real = criterionGAN(pred_real, True)

		# loss of real and fake 

		loss_d = (loss_d_fake + loss_d_real) * 0.5

		loss_d.backward()

		optimizerDis.step()

		#Train the Generator

		optimizerGen.zero_grad()

		#generator fake the Discriminator

		fake_DayNight = torch.cat((real_Night, fake_Day), 1)
		pred_fake = dis.forward(fake_DayNight)
		loss_g_gan = criterionGAN(pred_fake, True)

		loss_g_l1 = criterionL1(fake_Day, real_Day) * lamb

		loss_g = loss_g_gan + loss_g_l1

		loss_g.backward()
		
		optimizerGen.step()

		
		print('\n')
		print('------------------------ ------------------------ ------------------------')

		print("------------------------ EPOCH [{}]({}/{}) : LOSS GEN = {:.4f}, LOSS DIS = {:.4f}------------------------".format(epoch, iteration, len(training_data_loader), loss_g.data[0], loss_d.data[0]))
		data = fake_Day.detach().data[0]
		data2 = real_Night.detach().data[0]
		string1 = "/home/mohzick/NightfallProject/TestOutputs/datasetTest/dayTest/test"
		string12 = "%d" % iteration
		stringExtension = ".jpg"
		string14 = string1 + string12 + stringExtension
		string2 = "/home/mohzick/NightfallProject/TestOutputs/datasetTest/nightTest/test"
		string22 = string2 + string12 + stringExtension
	
		saveImage(data.cpu(), string14)
		saveImage(data2.cpu(), string22)	

gen = gen.cuda()
def test():
	
	'''for iteration, batch in enumerate(testing_data_loader, 1):

		real_Night_cpu, real_Day_cpu = batch[0], batch[1]
		real_Night.data.resize_(real_Night_cpu.size()).copy_(real_Night_cpu)
		real_Day.data.resize_(real_Day_cpu.size()).copy_(real_Day_cpu)

		fake_Day = gen(real_Night)

		data = fake_Day.detach().data[0]
		data2 = real_Night.detach().data[0]
		string1 = "/home/mohzick/NightfallProject/TestOutputs/realTest/dayTest/test"
		string12 = "%d" % iteration
		stringExtension = ".jpg"
		string14 = string1 + string12 + stringExtension
		string2 = "/home/mohzick/NightfallProject/TestOutputs/realTest/nightTest/test"
		string22 = string2 + string12 + stringExtension
	
		saveImage(data.cpu(), string14)
		saveImage(data2.cpu(), string22)'''
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
		#image_pred.save('test.jpg')
		#cv2.imshow('day', image_pred)
		#cv2.waitKey(0)
		

		print('yes')




def save(gen, dis):
	torch.save(gen, "genmodeltest.pth")
	torch.save(dis, "dismodeltest.pth")
	print("Model successfully saved.")



#for epoch in range(1, nbEpochs + 1):
	#train(epoch)

#save(gen, dis)

test()

end = time.time()
totalTime = end - start
print("Process time:", totalTime, "seconds")








