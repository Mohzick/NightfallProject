from PIL import Image
import os
import numpy
import argparse
from resizeimage import resizeimage

counter = 0

parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--resize', dest='imgResize', help='size of resized image',type=int, default=350)
parser.add_argument('--startpos', dest='startPos', help='cropping distance of top',type=int, default=250)
parser.add_argument('--divide', dest='divide', help='nb of division',type=int, default=4)
parser.add_argument('--inFolder', dest='inFolder', help='Input images folder', default='.\\trainTyphoon')
parser.add_argument('--outFolder', dest='outFolder', help='Output images folder', default='.\\trainTyphoonCropTest')

args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg,  getattr(args, arg))

if __name__=='__main__':

    inFolder = args.inFolder
    outFolder = args.outFolder

    if (inFolder == None):
        print("ciao")

    #file list inFolder
    for entry in os.scandir(inFolder):
        if entry.is_file():
            originalImage = Image.open(entry.path)
            print(entry.path)

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

                    if not os.path.isdir(outFolder):
                        os.makedirs(outFolder)

                    outputImg.save(outFolder + "\\out%d.jpg" % counter)