import pyzed.sl as sl
import numpy as np
import cv2
import glob

def calibrate_camera(fps, image, result):
    
    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = fps

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(-1)

        
    # To capture image
    #
    # image = sl.Mat()
    # if zed.grab() == SUCCESS:
    #   # A new image is available if grab() returns SUCCESS
    #   zed.retrieve_image(image, sl.VIEW.LEFT) # Retrieve the left image


    calibration_params = zed.get_camera_information().calibration_parameters
    # Focal length of the left eye in pixels
    focal_left_x = calibration_params.left_cam.fx
    # First radial distortion coefficient
    k1 = calibration_params.left_cam.disto[0]
    # Translation between left and right eye on z-axis
    tz = calibration_params.T.z
    # Horizontal field of view of the left eye in degrees
    h_fov = calibration_params.left_cam.h_fov


    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob(image)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

    #         # Draw and display the corners
    #         img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
    #         cv2.imshow('img',img)
    #         cv2.waitKey(500)


    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite(result,dst)

