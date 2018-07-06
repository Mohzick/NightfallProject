from PIL import Image
import os
import glob
import numpy
import argparse
from resizeimage import resizeimage

counter = 0

parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--resize', dest='imgResize', help='size of resized image',type=int, default=350)
parser.add_argument('--startpos', dest='startPos', help='cropping distance of top',type=int, default=250)
parser.add_argument('--divide', dest='divide', help='nb of division',type=int, default=4)

args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg,  getattr(args, arg))

if __name__=='__main__':

    imgDir = '.\\trainRain'
    saveDir = '.\\trainRainCrop'
    fileName = '*.JPG'

    fileList = glob.glob(os.path.join(imgDir,fileName))

    for truc, filePath in enumerate(fileList):
        
        originalImage = Image.open(filePath)
        print(filePath)

        imgwidth, imgheight = originalImage.size

        divide = args.divide
        #cropping images from one 4K image
        height = int(round(imgwidth/divide, 0))
        width =  int(round(imgwidth/divide, 0))

        #starting point for each of the n images separated by 600 pix
        startPosX = numpy.arange(0, imgwidth, 850)
        startPosY = args.startPos    #removing the top part

        croppedImg = Image.new('RGB', (width,height), 2047)

        #iterate over the x positions
        for x in startPosX:

            #crop the image if the cropped dimensions are still within range of the image's width
            #if it went beyond the image's width, the output would be filled with red for unexisting regions
            if (x+width < imgwidth):
                box = (x, startPosY, width+x, height+startPosY)
                croppedImg.paste(originalImage.crop(box))

                #resizing the image
                imgResize = args.imgResize
                outputImg = resizeimage.resize_cover(croppedImg, [imgResize, imgResize])

                #saving image
                counter += 1

                path = saveDir
                if not os.path.isdir(path):
                    os.makedirs(path)
                fileName = '\\out'  
                extension = ".jpg"
                outputPath = path + fileName + str(counter) + extension
                outputImg.save(outputPath)