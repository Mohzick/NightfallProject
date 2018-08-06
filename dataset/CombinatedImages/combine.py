'''Based on combine_A_and_B.py from 
https://github.com/phillipi/pix2pix/blob/master/scripts/combine_A_and_B.py
'''

import os
import numpy as np
import argparse
import cv2

parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--fold_A', dest='fold_A', help='input directory for image A', type=str, default='.\\DN1')
parser.add_argument('--fold_B', dest='fold_B', help='input directory for image B', type=str, default='.\\DN1')
parser.add_argument('--fold_AB', dest='fold_AB', help='output directory', type=str, default='./Output')
parser.add_argument('--num_imgs', dest='num_imgs', help='number of images',type=int, default=116)
parser.add_argument('--use_AB', dest='use_AB', help='if true: (0001_A, 0001_B) to (0001_AB)',action='store_true')
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg,  getattr(args, arg))


#img_fold_A = '.\\DN1\\Day'
#img_fold_B = '.\\DN1\\Night'

img_fold_A = args.fold_A
img_fold_B = args.fold_B

print("Path B = ")
print(img_fold_B)

img_list = os.listdir(img_fold_A)

if args.use_AB:
    img_list = [img_path for img_path in img_list if '_A.' in img_path]

num_imgs = min(args.num_imgs, len(img_list))

#print('split = %s, use %d/%d images' % (sp, num_imgs, len(img_list)))

img_fold_AB = args.fold_AB

if not os.path.isdir(img_fold_AB):
    os.makedirs(img_fold_AB)

#print('split = %s, number of images = %d' % (sp, num_imgs))

for n in range(num_imgs):
    name_A = img_list[n]
    path_A = os.path.join(img_fold_A, name_A)


    if args.use_AB:
        name_B = name_A.replace('_A.', '_B.')

    else:
        name_B = name_A

    path_B = os.path.join(img_fold_B, name_B)

    #print("#######PAAAAAAAAATH A = ")
    #print(os.path.isfile(path_A))

    if os.path.isfile(path_A) and os.path.isfile(path_B):

        name_AB = name_A


        if args.use_AB:
            name_AB = name_AB.replace('_A.', '.') # remove _A
        path_AB = os.path.join(img_fold_AB, name_AB)
        im_A = cv2.imread(path_A, cv2.IMREAD_COLOR)
        im_B = cv2.imread(path_B, cv2.IMREAD_COLOR)
        im_AB = np.concatenate([im_A, im_B], 1)
        cv2.imwrite(path_AB, im_AB)