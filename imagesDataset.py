from os import listdir
from os.path import join
from PIL import Image

import torch.utils.data as data
import torchvision.transforms as transforms
import numpy as np

size = 352 #size of the input and ouput, it's a square

#function useful to process images

def isImage(filename):
    return any(filename.endswith(extension) for extension in [".png", ".jpg", ".jpeg", ".JPG", ])

def loadImage(filepath):
    img = Image.open(filepath).convert('RGB')
    img = img.resize((size, size), Image.BICUBIC)
    return img

def saveImage(image_tensor, filename):
    image_numpy = image_tensor.float().numpy()
    image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
    image_numpy = image_numpy.astype(np.uint8)
    image_pil = Image.fromarray(image_numpy)
    image_pil.save(filename)
    print("Image saved as {}".format(filename))





#Class containing many functions allowing to create a dataset from the folder we are in

class createDataset(data.Dataset):

    def __init__(self, image_folder):
        super(createDataset, self).__init__()
        self.day_path = join(image_folder, "Day")
        self.night_path = join(image_folder, "Night")
        self.images_name = [n for n in listdir(self.night_path) if isImage(n)]

        self.transformation = transforms.Compose([transforms.ToTensor(), 
                                                 transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]) 

    #function allowing to load image

    def __getitem__(self, index):
        input = loadImage(join(self.night_path, self.images_name[index]))
        input = self.transformation(input)
        target = loadImage(join(self.day_path, self.images_name[index]))
        target = self.transformation(target)

        return input, target

    #function allowing us to know the length of a dataset

    def __len__(self):
        return len(self.images_name)


#functions allowing us to load either the training set to train our network 
#or to test one already trained

def getTrainingDataset(folderpath):
    trainingFolder = join(folderpath, "training")

    return createDataset(trainingFolder)

def getTestingDataset(folderpath):
    trainingFolder = join(folderpath, "testing")

    return createDataset(trainingFolder)




















































