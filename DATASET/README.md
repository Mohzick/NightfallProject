# Intro

This is a dataset of night and day pictures of the same location captured for Project Nightfall.

The night and day pairs are in different folders. A python script is also included in order to load the dataset into a Pytorch NN.

## 1. Content

DN1 is the first attempt of capture (see section 2 for capture method)

DN2 is the highest quality set of pictures and also the most numerous. It was captured with the same method as DN1.
However, the robot's path was planned more carefully and all lit screens were shut down to ensure darkness.

DN3 was captured using another method: the camera was tethered to the computer and 4K screenshots were made using MPC-HC.
It produced rather a low-quality result (this doesn't really matter since everything was resized afterwards).
However, no exposure adustments have been made: this could be a problem for machine learning, with the numerous artifacts in the night pictures.

DN4_FullDark: as its name implies, IT contains the pictures that received no or insufficient illumination during night. We will see if those are exploitable.

Further dataset types will come, depending on the needs of the project.


## 2. Methodology

For image capture, I used a Ricoh Theta S camera producing 360 degrees, 4K pictures. The Ricoh was mounted on a Roomba iRobot driven by a tethered laptop. 
The Roomba was guided by masking tape on the lab floor, using Python/OpenCV for its line recognition algorithm.

The 360 pictures were then post-processed in Adobe Photoshop with various scripts, then renamed with the help of Advanced Renamer.

Some further research may be needed to improve the process' automation.
