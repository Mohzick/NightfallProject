# Intro

This is a dataset of night and day pictures of the same location captured for Project Nightfall.

The night and day pairs are combinated into a single image with a size of 700x350px. A python script is also included in order to combine a pair of images. Should you want to use them separately, please check the RAW folder.

## 1. Content

The folders are 

DN1 is the first attempt of capture (see section 2 for capture method)

DN2 is the highest quality set of pictures and also the most numerous. It was captured with the same method as DN1.
However, the robot's path was planned more carefully and all lit screens were shut down to ensure darkness.

DN3 was captured using another method: the camera was tethered to the computer and 4K screenshots were made using MPC-HC.
It produced rather a low-quality result (this doesn't really matter since everything was resized afterwards).
However, no exposure adustments have been made: this could be a problem for machine learning, with the numerous artifacts in the night pictures.

DN4_Dark: as its name implies, IT contains the pictures that received no or insufficient illumination during night. We will see if those are exploitable.

DN5_all is a combination of DN1 and DN2 which are relatively similar datasets. It yields pretty good results when feeded to the neural network. Other dataset of this kind will be made in the near future.

DN6 is a combination of DN1 and DN2, cut into four sub-photos instead of being resized. The idea behind DN6 is that the other datasets required to images to be resized from 1440px to 350px, in order to help the neural network by reducing the amount of calculations needed. A lot of data is lost and wasted this way. Instead, what can be done is to crop the full images into smaller ones, eliminating the need for resizing. 
DN6 especially focuses on details. Each image size is 450x450 px (4 images from a 900x900 image). To be tested. 

DN7 is a combination of DN5 and resized DN6 (both sizes are 350x350 px). It gives details (4/5 of the dataset) and a general view (1/5) of the room at the same time. It is the most extensive dataset as for now, containing 1084 pairs (865 from DN6 and 219 from DN5). To be tested.

Further dataset types will come, depending on the needs of the project.


## 2. Methodology

For image capture, I used a Ricoh Theta S camera producing 360 degrees, 4K pictures. The Ricoh was mounted on a Roomba iRobot driven by a tethered laptop. The Roomba was guided by masking tape on the lab floor, using Python/OpenCV for its line recognition algorithm.

The 360 pictures were then post-processed in Adobe Photoshop with various scripts, then renamed with the help of Advanced Renamer.

As the lab isn't able to be fully in the dark, the photos nearly all have illumination from outside. This should be close to realistic conditions. Furthermore, the webcam is not able to capture any image under a certain luminosity threshold. Thus, the exterior illumination should be seen as an advantage of this dataset. 

Some fully dark images are also randomly included. They are to be removed if they do not prove to be useful for the training. 

Some further research may be needed to improve the process' automation.
