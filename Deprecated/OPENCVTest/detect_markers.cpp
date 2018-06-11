/*
By downloading, copying, installing or using the software you agree to this
license. If you do not agree to this license, do not download, install,
copy or use the software.

                          License Agreement
               For Open Source Computer Vision Library
                       (3-clause BSD License)

Copyright (C) 2013, OpenCV Foundation, all rights reserved.
Third party copyrights are property of their respective owners.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  * Neither the names of the copyright holders nor the names of the contributors
    may be used to endorse or promote products derived from this software
    without specific prior written permission.

This software is provided by the copyright holders and contributors "as is" and
any express or implied warranties, including, but not limited to, the implied
warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall copyright holders or contributors be liable for
any direct, indirect, incidental, special, exemplary, or consequential damages
(including, but not limited to, procurement of substitute goods or services;
loss of use, data, or profits; or business interruption) however caused
and on any theory of liability, whether in contract, strict liability,
or tort (including negligence or otherwise) arising in any way out of
the use of this software, even if advised of the possibility of such damage.
*/


#include <opencv2/highgui.hpp>
#include <opencv2/aruco.hpp>
#include "detect_markers.h"
#include <opencv2/calib3d/calib3d.hpp>
#include <iostream>

#include "robot.h"



using namespace std;
using namespace cv;

namespace {
const char* about = "Basic marker detection";
const char* keys  =
        "{d        |       | dictionary: DICT_4X4_50=0, DICT_4X4_100=1, DICT_4X4_250=2,"
        "DICT_4X4_1000=3, DICT_5X5_50=4, DICT_5X5_100=5, DICT_5X5_250=6, DICT_5X5_1000=7, "
        "DICT_6X6_50=8, DICT_6X6_100=9, DICT_6X6_250=10, DICT_6X6_1000=11, DICT_7X7_50=12,"
        "DICT_7X7_100=13, DICT_7X7_250=14, DICT_7X7_1000=15, DICT_ARUCO_ORIGINAL = 16,"
        "DICT_APRILTAG_16h5=17, DICT_APRILTAG_25h9=18, DICT_APRILTAG_36h10=19, DICT_APRILTAG_36h11=20}"
        "{v        |       | Input from video file, if ommited, input comes from camera }"
        "{ci       | 0     | Camera id if input doesnt come from video (-v) }"
        "{c        |       | Camera intrinsic parameters. Needed for camera pose }"
        "{l        | 0.1   | Marker side lenght (in meters). Needed for correct scale in camera pose }"
        "{dp       |       | File of marker detector parameters }"
        "{r        |       | show rejected candidates too }"
        "{refine   |       | Corner refinement: CORNER_REFINE_NONE=0, CORNER_REFINE_SUBPIX=1,"
        "CORNER_REFINE_CONTOUR=2, CORNER_REFINE_APRILTAG=3}";
}

/**
 */
static bool readCameraParameters(string filename, Mat &camMatrix, Mat &distCoeffs) {
    FileStorage fs(filename, FileStorage::READ);
    if(!fs.isOpened())
        return false;
    fs["camera_matrix"] >> camMatrix;
    fs["distortion_coefficients"] >> distCoeffs;
    return true;
}

/**
 */
static bool readDetectorParameters(string filename, Ptr<aruco::DetectorParameters> &params) {
    FileStorage fs(filename, FileStorage::READ);
    if(!fs.isOpened())
        return false;
    fs["adaptiveThreshWinSizeMin"] >> params->adaptiveThreshWinSizeMin;
    fs["adaptiveThreshWinSizeMax"] >> params->adaptiveThreshWinSizeMax;
    fs["adaptiveThreshWinSizeStep"] >> params->adaptiveThreshWinSizeStep;
    fs["adaptiveThreshConstant"] >> params->adaptiveThreshConstant;
    fs["minMarkerPerimeterRate"] >> params->minMarkerPerimeterRate;
    fs["maxMarkerPerimeterRate"] >> params->maxMarkerPerimeterRate;
    fs["polygonalApproxAccuracyRate"] >> params->polygonalApproxAccuracyRate;
    fs["minCornerDistanceRate"] >> params->minCornerDistanceRate;
    fs["minDistanceToBorder"] >> params->minDistanceToBorder;
    fs["minMarkerDistanceRate"] >> params->minMarkerDistanceRate;
    fs["cornerRefinementMethod"] >> params->cornerRefinementMethod;
    fs["cornerRefinementWinSize"] >> params->cornerRefinementWinSize;
    fs["cornerRefinementMaxIterations"] >> params->cornerRefinementMaxIterations;
    fs["cornerRefinementMinAccuracy"] >> params->cornerRefinementMinAccuracy;
    fs["markerBorderBits"] >> params->markerBorderBits;
    fs["perspectiveRemovePixelPerCell"] >> params->perspectiveRemovePixelPerCell;
    fs["perspectiveRemoveIgnoredMarginPerCell"] >> params->perspectiveRemoveIgnoredMarginPerCell;
    fs["maxErroneousBitsInBorderRate"] >> params->maxErroneousBitsInBorderRate;
    fs["minOtsuStdDev"] >> params->minOtsuStdDev;
    fs["errorCorrectionRate"] >> params->errorCorrectionRate;
    return true;
}

/*
 * Main
 * This is the main. Nothing fancy
 */
int main(int argc, char *argv[]) {

	markerDetect(argc, argv);

}

/*
 * Detect if the marker isn't in the center of the image.
 * Returns 1 or 2 if it is on the left, 3 or 4 if it is on the right
 * and 0 if it is centered.
 */
int whereIsMarker(vector< vector< Point2f > > corners)
{
	int position = -1;
	vector < Point2f > points;
	for (auto cornerlist : corners)
	{
		//cornerlist's siwe should always be 1, since we're detecting one marker at a time
		for (auto cornerPoint : cornerlist)
		{
			points.push_back(cornerPoint); //the four corners are stored in a 4-elents vector
		}
	}

	Point2f midPoint;
	if (points.size() == 4)	//Now we can compute the center of the marker as well as its size
	{
		midPoint.x = (points[0].x + points[2].x) / 2;
		midPoint.y = (points[1].y + points[3].y) / 2;
	}

	//cout << "midpoint.x = " << midPoint.x << endl;
	//cout << "midpoint.y = " << midPoint.y << endl;
	
	if (midPoint.x > 300 && midPoint.x < 360){
		//cout << "En plein dans le mille mon gars!" << endl;
		position = 0;
	}
	else if (midPoint.x < 300 && midPoint.x > 200){
		position = 1;
	}
	else if (midPoint.x < 200 && midPoint.x > 0){
		position = 2;
	}
	else if (midPoint.x > 360 && midPoint.x < 460){
		position = 3;
	}
	else if (midPoint.x > 460 && midPoint.x < 600){
		position = 4;
	}
	else{
		//midPoint is not in the picture's frame
		//cout << "DEBUG: Webcam feed has no apparent marker!" << endl;
	}

	return position;
}


/*
 * Get the narker's id. Should return the first one
 * TODO: the case where there's more than one
 */
int getCurrentId(vector< int > ids)
{
	int currentId = -1;
	if (ids.size() == 1){
		currentId = ids[0];
	}
	return currentId;
}

char recenterRobot(int markerRelativePosition)
{

	char robotOrder;
	if (markerRelativePosition != -1)
	{
		if (markerRelativePosition == 1)
		{
			robotOrder = 'r';
		}
		else if (markerRelativePosition == 2)
		{
			robotOrder = 'r';
		}

		else if (markerRelativePosition == 3)
		{
			robotOrder = 'l'; //go left a bit
		}

		else if (markerRelativePosition == 4)
		{
			robotOrder = 'l'; //go left a lot
		}

		else if (markerRelativePosition == 0)
		{
			robotOrder = 'f'; //go straight
		}
	}

	return robotOrder;
}


char goLeft(vector< vector< Point2f > > corners)
{
	return 'l';

}

char goRight(vector< vector< Point2f > > corners)
{
	return 'r';
}


/** Main marker detection function
 */
int markerDetect(int argc, char *argv[]) {

	//robot start. Useless? but used in Sakata sensei's program so........... idk? >.>
	start();

	//detection functions start
    CommandLineParser parser(argc, argv, keys);
    parser.about(about);

    if(argc < 2) {
        parser.printMessage();
        return 0;
    }

    int dictionaryId = parser.get<int>("d");
    bool showRejected = parser.has("r");
    bool estimatePose = parser.has("c");
    float markerLength = parser.get<float>("l");

    Ptr<aruco::DetectorParameters> detectorParams = aruco::DetectorParameters::create();
    if(parser.has("dp")) {
        bool readOk = readDetectorParameters(parser.get<string>("dp"), detectorParams);
        if(!readOk) {
            cerr << "Invalid detector parameters file" << endl;
            return 0;
        }
    }

    if (parser.has("refine")) {
        //override cornerRefinementMethod read from config file
        detectorParams->cornerRefinementMethod = parser.get<int>("refine");
    }
    std::cout << "Corner refinement method (0: None, 1: Subpixel, 2:contour, 3: AprilTag 2): " << detectorParams->cornerRefinementMethod << std::endl;

    int camId = parser.get<int>("ci");

    String video;
    if(parser.has("v")) {
        video = parser.get<String>("v");
    }

    if(!parser.check()) {
        parser.printErrors();
        return 0;
    }

    Ptr<aruco::Dictionary> dictionary =
        aruco::getPredefinedDictionary(aruco::PREDEFINED_DICTIONARY_NAME(dictionaryId));

    Mat camMatrix, distCoeffs;
    if(estimatePose) {
        bool readOk = readCameraParameters(parser.get<string>("c"), camMatrix, distCoeffs);
        if(!readOk) {
            cerr << "Invalid camera file" << endl;
            return 0;
        }
    }

    VideoCapture inputVideo;
    int waitTime;
    if(!video.empty()) {
        inputVideo.open(video);
        waitTime = 0;
    } else {
        inputVideo.open(camId);
        waitTime = 10;
    }

    double totalTime = 0;
    int totalIterations = 0;

	char previousRobotOrder ='t';

	//my variable. Used to skip some frames before sending an instruction to the robot
	//if we send too many instructions at the same time, the robot will just shut down 
	int iterLoop = 0;

	//main while loop
    while(inputVideo.grab()) {

        Mat image, imageCopy;
        inputVideo.retrieve(image);

        double tick = (double)getTickCount();

        vector< int > ids;
		int currentId = -1; //the marker's id. We will have a 'go straight' marker, and 'go left' and 'go right' ones.
        vector< vector< Point2f > > corners, rejected;
        vector< Vec3d > rvecs, tvecs;

        //From here: detect markers and estimate pose
		/*main detection call:
			- image is the camera feed. Can be a static png or whatever the webcam feed is (some kind of pointer).
			- dictionary is the dict that contains all the used markers.
			- corners is the list of corners of the detected markers.
			- ids is the list of ids of each of the detected markers in corners.

			The fourth parameter is the object of type DetectionParameters (obscure stuff, look at the official website)
			This object includes all the parameters that can be customized during the detection process.
			
			The final parameter, rejectedCandidates, is a returned list of marker candidates.

			Source: https://docs.opencv.org/master/d5/dae/tutorial_aruco_detection.html
		*/
		aruco::detectMarkers(image, dictionary, corners, ids, detectorParams, rejected);

		//Get the id of the first detected marker.1: go straight, 2: go left, 3: go right, 4: stop
		currentId = getCurrentId(ids);
		char robotOrder = 's'; //cout << "Current id =" << currentId << endl; //this is supposed to work correctly. Will have to test for several markers at the same time

		//Detect the position of the marker
		//f-forward,b-back, r-right, l-left, s-stop

		int markerRelativePosition = -1;
		markerRelativePosition = whereIsMarker(corners);
						//cout << "marker relative position : " << markerRelativePosition << endl;
		
		if (markerRelativePosition > 0) //when the robot is not straight
		{								//IGNORE marker id orders (left, right etc)
		
			robotOrder = recenterRobot(markerRelativePosition);
			cout << "Recentering robot... with movement to the " << robotOrder << endl;
		}

		//if robot is straight then proceed with the instruction the marker gives
		else if (corners.size() > 0) 
		{
			if (currentId == 1)
			{
				robotOrder = 'f';
			}
			else if (currentId == 2)
			{
				robotOrder = 'l';
			}
			else if (currentId == 3)
			{
				robotOrder = 'r';
			}
			else if (currentId == 4)
			{
				robotOrder = 's';
			}
			else if (currentId == 0)
			{
				robotOrder = 'b';
			}
			cout << "Moving the robot to the " << robotOrder << "!" << endl;

		}
		else{
			//cout << "DEBUG: No marker detected!" << endl;
		}
		//robot movement
		//objective would be to adjust position depending on the marker's position

		//std::chrono::milliseconds timespan(100); // or whatever. 300 works well but laggy as fuck
		//std::this_thread::sleep_for(timespan); //DEPRECATED: replacing this with iterLoop.
		if (iterLoop == 60)
		{			
			if (previousRobotOrder != 's')
			{
				robot(robotOrder, 10);
				cout << "sending an " << robotOrder << " order to robot!" << endl;

			}
			
			if (robotOrder != 's')
			{
				//	robot('s', 20);
			}
			iterLoop = 0;

			previousRobotOrder = robotOrder;

		}
	
		//estimating marker position using the corners. Triggered by estimatePose which itself is True when there is a -c argument (camera intrinsic position)
		//for now we're not going into this because estimatePose is always false (no -c argv)
		if (estimatePose && ids.size() > 0)
		{
			cout << "DEBUG: this is not supposed to appear. 2" << endl;
			//estimatePoseSingleMarkers's output is rvecs and tvecs, which gives you the orientation of the camera relative to the marker.
			//Since we want the orientation of the marker relative to the camera, we need to invert those values.
			aruco::estimatePoseSingleMarkers(corners, markerLength, camMatrix, distCoeffs, rvecs,
				tvecs);
		}	
		
		//calculating computing time.
		//This is useful to detect robot computing loops bugs.
		//For now it's around 140ms for one detection (even more with the sleep function)
        double currentTime = ((double)getTickCount() - tick) / getTickFrequency();
        totalTime += currentTime;
        totalIterations++;
        if(totalIterations % 30 == 0) {
            cout << "Detection Time = " << currentTime * 1000 << " ms "
                 << "(Mean = " << 1000 * totalTime / double(totalIterations) << " ms)" << endl;
        }

        // draw results on camera feed. We need to somehow remove the marker from the photo.
        image.copyTo(imageCopy);
        if(ids.size() > 0) {
            aruco::drawDetectedMarkers(imageCopy, corners, ids);

            if(estimatePose) {
                for(unsigned int i = 0; i < ids.size(); i++)
                    aruco::drawAxis(imageCopy, camMatrix, distCoeffs, rvecs[i], tvecs[i],
                                    markerLength * 0.5f);
            }
        }

        if(showRejected && rejected.size() > 0)
            aruco::drawDetectedMarkers(imageCopy, rejected, noArray(), Scalar(100, 0, 255));

        imshow("out", imageCopy);
        char key = (char)waitKey(waitTime);
		iterLoop++;
        if(key == 27) break;
    }

    return 0;
}
