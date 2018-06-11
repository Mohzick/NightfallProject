#ifndef ROBOT_H    // To make sure you don't declare the function more than once by including the header multiple times.
#define ROBOT_H
void start();
void foward(unsigned char); //forward function
void back(); //back function
void left(unsigned char); //turn left
void right(unsigned char); //turn right
void stop(); //stop


int robot(char c, unsigned char v);

#endif
