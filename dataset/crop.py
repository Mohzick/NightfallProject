


'''
img_list = os.listdir('.\\DN1\\Day')

num_imgs = min(args.num_imgs, len(img_list))

#print('split = %s, use %d/%d images' % (sp, num_imgs, len(img_list)))

for n in range(num_imgs):
    name_A = img_list[n]
    path_A = os.path.join(img_fold_A, name_A)

    else:
        name_B = name_A

    path_B = os.path.join(img_fold_B, name_B)

    #print("#######PAAAAAAAAATH A = ")
    #print(os.path.isfile(path_A))

    if os.path.isfile(path_A) and os.path.isfile(path_B):


        if args.use_AB:
            name_AB = name_AB.replace('_A.', '.') # remove _A
        path_AB = os.path.join(img_fold_AB, name_AB)
        im_A = cv2.imread(path_A, cv2.IMREAD_COLOR)
        im_B = cv2.imread(path_B, cv2.IMREAD_COLOR)
        im_AB = np.concatenate([im_A, im_B], 1)
        cv2.imwrite(path_AB, im_AB)

'''
from PIL import Image
import os
import glob

counter = 0

if __name__=='__main__':

    imgDir = '.\\TestCrop'
    saveDir = '.\\Outputs'

    filelist = glob.glob(os.path.join(imgdir,basename))

    for filenum,infile in enumerate(filelist):

        # infile='/Users/alex/Documents/PTV/test_splitter/cal/Camera 1-1-9.tif'
        
        originalImage = Image.open(infile)
        print(infile)

        imgwidth, imgheight = originalImage.size

        #cropping 4 images from one 4K image
        height = int(round(imgwidth/4, 0))
        width =  int(round(imgwidth/4, 0))

        #starting point for each of the 4 images
        startPosX = [0, imgwidth/2, imgwidth/3, imgwidth/4]
        startPosY = 250    #removing the top part

        start_num = 0

        croppedImg = Image.new('RGB', (width,height), 2047)

        #iterate over the x positions
        for x in startPosX:
            box = (x, startPosY, width+x, height+startPosY)
            croppedImg.paste(originalImage.crop(box))

            #resizing croppedImg


            #saving image
            counter += 1
            path = ".\\TestCrop\\output"
            path2 = ".jpg"
            path3 = path + str(counter) + path2
            croppedImg.save(path3)