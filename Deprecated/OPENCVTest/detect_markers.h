#pragma once

#include <opencv2/highgui.hpp>
#include <opencv2/aruco.hpp>
#include <iostream>

using namespace std;
using namespace cv;


int markerDetect(int argc, char *argv[]);

int whereIsMarker(vector< vector< Point2f > > corners);

int getCurrentId(vector< int > ids);


//recenter robot. Returns a direction
char recenterRobot(int markerRelativePosition);

//Rush left 45 degrees
char goLeft(vector< vector< Point2f > > corners);


//Rush right 45 degrees
char goRight(vector< vector< Point2f > > corners);