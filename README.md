# NightfallProject

**Nightfall Project**'s objective is to transform a photo (for example night to day or rainy to sunny) using machine learning.
This project was developped during a 3-months long internship at CARE Lab (Nara Institute of Science and Technology, Nara, Japan) by a team of two, [@Mohzick](https://github.com/Mohzick) and [@minh-n](https://github.com/minh-n).

## Introduction and motivations

Nightfall Project originally aims to convert a night video into a day video, using an image generating neural network. Transforming night to day has several applications in automated vehicles (to have a clear image of the night, allowing better visibility), surveillance and even tourism or AR attractions. For example, a future tourist will be able to clear rain from a landscape to take the perfect picture. 

This project tackles the basics of machine learning and computer vision. It is mostly a learning experience and reuses the work of Nvidia who developped the main ideas behind the Pix2Pix and CycleGAN machine learning algorithms. 

This project is broadly divided into three parts: in order to train the neural network, I created a dataset composed of various kind of images. Some of them are pairs of day and night images captured by a 360 camera. Some others, like the rain dataset, have been captured by a smartphone and are all unpaired images. The seccond part involves understanding and implementing the Pix2pix and CycleGAN algorithms and creating a model using the dataset. Finally, a real-time application using a PC webcam can be created.

## The application

The final product of this project is a real-time Python application displaying a webcam feed and the processed output of the night-to-day neural network. A video demo is available at [insert gitHub address here]. It is only able to convert the laboratory’s environment because of the very specific training dataset [@minh-n](https://github.com/minh-n) created. 

## Running the application

### Prerequisites

The conversion application can be runned as is on Linux and needs the following libraries:

```
Python 3.6
CUDA version ?
PyTorch 0.4
PIL and OpenCV 
```

The dataset processing scripts only needs `PIL` & `OpenCV`.

### Shell commands

```
python test.py --args @Mohzick pls do this
```

## Machine learning 

The Pix2Pix neural network can be trained using a dataset formatted using the available scripts. The dataset needs to be separated into two folders of paired images (Day and Night or any other transformation). The images' size needs to be 350x350. A good number of pairs would be around 1000 (we could only use the 600 available for the final application).  

## Technologies used

With the help of a programmable cleaner robot and an omnidirectional camera, we have captured many pairs of the corresponding night and day-time images from the same viewpoint.  [![A video of the robot in action](https://img.youtube.com/vi/vov4H4KSB8A/0.jpg)](https://www.youtube.com/watch?v=vov4H4KSB8A)


## Future work

A standalone Windows app could be developed in order to use it with a Hololens type of device. Other datasets can be created to make the application useable in various kinds of environments. 

## Credits

We would like to thank the team behind Pix2Pix, CycleGAN, PyTorch and CUDA, as well as the teachers and students of CARE Lab. Without them, this whole project would not have been possible. 

