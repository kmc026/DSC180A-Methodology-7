#### Autonomous Vehicles Team 5 Computer Vision and ROS Package

Ka Ming Chan
A13771194

The test image data is found online, since our team is currently having issue with using NoMachine to operate the hardware assembly which is composed of the camera and the Jetson. We seemed to be unable to collect our own data yet. I am a remote student who does not have the hardwares in hand, and therefore I chose this alternative way. The code and sample data are found online in a Medium article, in which the author states that they are free to use. I used it as an example to gain experience on creating a disparity map between two pictures taken by the same stereo camera, and then generating a 3D point cloud out of that disparity map. This process is the key for meauring depth, or the distances of the objects inside an image, which reinforces object recognition. I was responsible for researching the theories of depth in stereo images.

For this assignment, my code's target is to create the sample_3d_pointcloud.ply file in the "results" folder.

References:
https://medium.com/analytics-vidhya/depth-sensing-and-3d-reconstruction-512ed121aa60
https://github.com/umangkshah/notebooks/tree/master/3d_reconstruction