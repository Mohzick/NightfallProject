import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np



def get_normalization_layer(normalization):

	if normalization == 'batch':
		normalization_layer = nn.BatchNorm2d


	elif normalization == 'instance':
		normalization_layer = nn.InstanceNorm2d

	else:
		print('The normalization layer inputed doesnt exist here : %s' % normalization)

	return normalization_layer

# weights are initiated depending on the class (function called by the Generator and Discriminator)

def weights_init(m):
	classname = m.__class__.__name__
	if classname.find('Conv') != -1:
		m.weight.data.normal_(0.0, 0.02)
	elif classname.find('BatchNorm2d') != -1 or classname.find('InstanceNorm2d') != -1:
		m.weight.data.normal_(1.0, 0.02)
		m.bias.data.fill_(0)


# Block used in a neuralnet for the generator

class NeuralnetBLock(nn.Module):

	def __init__(self, dim, normalization_layer):
		super(NeuralnetBLock, self).__init__()
		self.conv_block = self.build_conv_block(dim, normalization_layer)

	def build_conv_block(self, dim, normalization_layer):
		conv_block = []

		conv_block += [nn.Conv2d(dim, dim, kernel_size = 3, padding = 1),
					   normalization_layer(dim, affine = True),
					   nn.ReLU(True)]

		conv_block += [nn.Conv2d(dim, dim, kernel_size = 3, padding = 1),
					   normalization_layer(dim, affine = True)]

		return nn.Sequential(*conv_block)

	def forward(self, x):
		out = x + self.conv_block(x)
		return out


#Generator Neural Network

class NeuralnetGen(nn.Module): 
	def __init__(self, input_rgb, output_rgb, gen_filters, normalization_layer = nn.BatchNorm2d, n_blocks=6, gpu_ids=[]):
		super(NeuralnetGen, self).__init__()
		self.input_rgb = input_rgb
		self.output_rgb = output_rgb
		self.gen_filters = gen_filters
		self.gpu_ids = gpu_ids

		model = [nn.Conv2d(input_rgb, gen_filters, kernel_size = 7, padding = 3),
				 normalization_layer(gen_filters, affine = True),
				 nn.ReLU(True)]
		
		n_downsampling = 2

		for i in range(n_downsampling):
			mult = 2**i
			model += [nn.Conv2d(gen_filters * mult, gen_filters * mult * 2, kernel_size = 3, stride = 2, padding = 1),
					  normalization_layer(gen_filters * mult * 2, affine = True),
					  nn.ReLU(True)]

		mult = 2**n_downsampling
		
		for i in range(n_blocks):
			model += [NeuralnetBLock(gen_filters * mult, normalization_layer = normalization_layer)]

		for i in range(n_downsampling):
			mult = 2**(n_downsampling - i)
			model += [nn.ConvTranspose2d(gen_filters * mult, int(gen_filters * mult / 2), 
										 kernel_size = 3, stride = 2, padding = 1, output_padding = 1),
					  normalization_layer(int(gen_filters * mult / 2), affine = True), 
					  nn.ReLU(True)]

		model += [nn.Conv2d(gen_filters, output_rgb, kernel_size = 7, padding = 3)]
		model += [nn.Tanh()]

		self.model = nn.Sequential(*model)

	def forward(self, input):
		if self.gpu_ids and isinstance(input.data, torch.cuda.FloatTensor):
			return nn.parallel.data_parallel(self.model, input, self.gpu_ids)
		else:
			return self.model(input)







def createGenerator(input_rgb, output_rgb, gen_filters, normalization = 'batch', gpu_ids = []):
	gen = None 
	norm_layer = get_normalization_layer(normalization = normalization)

	if len(gpu_ids) > 0:
		assert(torch.cuda.is_available())

	gen = NeuralnetGen(input_rgb, output_rgb, gen_filters, normalization_layer = norm_layer, n_blocks = 9, gpu_ids = gpu_ids)

	if len(gpu_ids) > 0:
		gen.cuda(gpu_ids[0])

	gen.apply(weights_init)

	return gen


# Discriminator Neural Network

class NeuralNetDiscr(nn.Module):
	def __init__(self, input_rgb, dis_filters, n_layers = 3, normalization_layer = nn.BatchNorm2d, gpu_ids = []):
		super(NeuralNetDiscr, self).__init__()
		self.gpu_ids = gpu_ids

		kw = 4
		padw = int (np.ceil((kw-1)/2))

		sequence = [
			nn.Conv2d(input_rgb, dis_filters, kernel_size = kw, stride = 2, padding = padw),
			nn.LeakyReLU(0.2, True)
		]

		nf_mult = 1
		nf_mult_prev = 1

		for n in range (1, n_layers):
			nf_mult_prev = nf_mult
			nf_mult = min(2**n, 8)

			sequence += [
				nn.Conv2d(dis_filters * nf_mult_prev, dis_filters * nf_mult, kernel_size = kw, stride = 2, padding = padw),
				normalization_layer(dis_filters * nf_mult, affine = True),
				nn.LeakyReLU(0.2, True)
			]

		nf_mult_prev = nf_mult
		nf_mult = min(2**n_layers, 8)

		sequence += [
			nn.Conv2d(dis_filters * nf_mult_prev, dis_filters * nf_mult, kernel_size = kw, stride = 1, padding = padw),
			normalization_layer(dis_filters * nf_mult, affine = True),
			nn.LeakyReLU(0.2, True)
		]

		sequence += [nn.Conv2d(dis_filters * nf_mult, 1, kernel_size=kw, stride=1, padding=padw)]

		self.model = nn.Sequential(*sequence)

	def forward(self, input):
		if len(self.gpu_ids) and isinstance(input.data, torch.cuda.FloatTensor):
			return nn.parallel.data_parallel(self.model, input, self.gpu_ids)
		else:
			return self.model(input)


def createDiscriminator(input_rgb, dis_filters, normalization = 'batch', gpu_ids = []):
	dis = None
	normalization_layer = get_normalization_layer(normalization = normalization)

	if len(gpu_ids) > 0:
		assert(torch.cuda.is_available())

	dis = NeuralNetDiscr(input_rgb, dis_filters, n_layers = 3, normalization_layer = normalization_layer, gpu_ids = gpu_ids)
	
	if len(gpu_ids) > 0:
		dis.cuda(gpu_ids[0])

	dis.apply(weights_init)

	return dis

# Function defining the GAN Loss using either LSGAN or normal GAN

class GANLoss(nn.Module):
	def __init__(self, lsgan = True, target_real_label = 1.0, target_fake_label = 0.0, tensor = torch.FloatTensor):
		super(GANLoss, self).__init__()
		self.real_label = target_real_label
		self.fake_label = target_fake_label
		self.real_label_var = None
		self.fake_label_var = None
		self.Tensor = tensor
		if lsgan:
			self.loss = nn.MSELoss()
		else:
			self.loss = nn.BCELoss()

	def get_target_tensor(self, input, isreal):
		target_tensor = None
		
		if isreal:
			create_label = ((self.real_label_var is None) or (self.real_label_var.numel() != input.numel()))

			if create_label:
				real_tensor = self.Tensor(input.size()).fill_(self.real_label)
				self.real_label_var = Variable(real_tensor, requires_grad = False)

			target_tensor = self.real_label_var

		else:
			create_label = ((self.fake_label_var is None) or (self.fake_label_var.numel() != input.numel()))
			
			if create_label:
				fake_tensor = self.Tensor(input.size()).fill_(self.fake_label)
				self.fake_label_var = Variable(fake_tensor, requires_grad = False)

			target_tensor = self.fake_label_var

		return target_tensor

	def __call__(self, input, isreal):
		target_tensor = self.get_target_tensor(input, isreal)
		return self.loss(input, target_tensor.cuda())


def print_net(network):
	param = 0
	for p in network.parameters():
		param += p.numel()

	#print(network)
	print('Number of parameters : %d' % param)
