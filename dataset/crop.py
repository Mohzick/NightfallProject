from PIL import Image
import os
import numpy
import argparse
from resizeimage import resizeimage

counter = 0

'''
parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--resize', dest='imgResize', help='size of resized image',type=int, default=350)
parser.add_argument('--startpos', dest='startPos', help='cropping distance of top',type=int, default=250)
parser.add_argument('--divide', dest='divide', help='nb of division',type=int, default=4)
parser.add_argument('--inFolder', dest='inFolder', help='Input images folder', default='.\\trainTest')
parser.add_argument('--outFolder', dest='outFolder', help='Output images folder', default='.\\croppedTest')

args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg,  getattr(args, arg))
'''

'''

    imgResize: the size of the (square) output image
    
    divide: the number of output images we want to get from the original image
    
    rangeX: the distance between each output image from another, wrt the original image (850 or roughly half recommended)
    
    in and out folders: the input and output folders

'''
def cropper(imgResize, divide, rangeX, inFolder, outFolder):


    if (inFolder == None):
        print("ERROR : No folder found in %s." % inFolder)

    #go through file list inFolder
    for entry in sorted(os.listdir(inFolder)):
        singleCrop(entry, imgResize, divide, rangeX, inFolder, outFolder)

'''
    Auxiliray function: crops one input image to produce several output images
'''
def singleCrop(fileInput, imgResize, divide, rangeX, inFolder, outFolder):

    if "jpg" in fileInput:
                originalImage = Image.open(inFolder + "/"+ fileInput) 
                
                print("Cropping {0} input image into {1} output image(s) ({2} x {3} px)...".format(fileInput, divide, imgResize, imgResize), end='\r')

                inputWidth, inputHeight = originalImage.size

                #cropping a certain number of images (value of divide) from one image

                if (divide > 1):    #getting an output image size, using the original image's size and the number of ouputs we want

                    outputHeight = int(round(inputWidth/divide, 0))
                    outputWidth =  int(round(inputWidth/divide, 0))

                    #starting point for each of the n images separated by %range pix
                    startPosX = numpy.arange(0, inputWidth, rangeX)
                    startPosY = 0     


                #one output wanted from the input
                else:              
                    outputHeight = inputHeight
                    outputWidth = outputHeight
                    startPosX = int(inputWidth/2 - outputHeight/2)   #since we want 1 output, we'll take the center 
                    startPosY = 0

                croppedImg = Image.new('RGB', (outputWidth,outputHeight), 2047)


                if isinstance(startPosX,(int)):
                    cropFromPosition(imgResize, startPosX, outputWidth, inputWidth, outputHeight, startPosY, croppedImg, originalImage, outFolder)  

                else:
                    #iterate over the x positions
                    for x in startPosX:
                        cropFromPosition(imgResize, x, outputWidth, inputWidth, outputHeight, startPosY, croppedImg, originalImage, outFolder)


'''
    Auxiliary function: crops and writes an image given the (numerous) parameters
'''
def cropFromPosition(imgResize, x, outputWidth, inputWidth, outputHeight, startPosY, croppedImg, originalImage, outFolder):
    
    global counter
    #crop the image if the cropped dimensions are still within range of the image's width
    #if it went beyond the image's width, the output would be filled with red for unexisting regions

    if (x+outputWidth < inputWidth):
        box = (x, startPosY, outputWidth+x, outputHeight+startPosY)
        croppedImg.paste(originalImage.crop(box))

        #resizing the image
        outputImg = resizeimage.resize_cover(croppedImg, [imgResize, imgResize])

        #saving image
        
        counter += 1
        if not os.path.isdir(outFolder):
            os.makedirs(outFolder)

        outputImg.save(outFolder + "/out%d.jpg" % counter)

