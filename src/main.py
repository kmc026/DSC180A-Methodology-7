import numpy as np
import cv2


def write_ply(fn, verts, colors):
    ply_header = '''ply
    format ascii 1.0
    element vertex %(vert_num)d
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    end_header
    '''
    out_colors = colors.copy()
    verts = verts.reshape(-1, 3)
    verts = np.hstack([verts, out_colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


def generate_3d_pointcloud(left_image_dir, right_image_dir, num_disparities, block_size, calibration_file_dir, result_dir):
    """
    Generates the 3D Point Cloud as .ply object in the results directory

    Parameters
    ----------
    left_image_dir : string
        The directory of the left image
    right_image_dir : string
        The directory of the right image
    num_disparities : int
        Parameter for stereo object
    block_size : int
        Parameter for stereo object
    calibration_file_dir : string
        The directory of the calibration file
    result_dir : string
        The directory for where the resulted .ply file should go

    Returns
    -------
    sample_3d_pointcloud.ply : ply file; 3D Object
        The 3D Point Cloud
    """

    #Read the two images in grayscale
    image1 = cv2.imread(left_image_dir, 0)
    image2 = cv2.imread(right_image_dir, 0)

    #Read the two images in color
    image1_colored = cv2.imread(left_image_dir, 1)
    image2_colored = cv2.imread(right_image_dir, 1)

    #Generate the disparity map
    stereo = cv2.StereoBM_create(numDisparities = num_disparities, blockSize = block_size)
    disparity = stereo.compute(image1, image2)
    disparity_result = disparity.copy()

    #Read in calibration
    matrix_type_1 = 'P2'
    matrix_type_2 = 'P3'

    calib_file = calibration_file_dir
    with open(calib_file, 'r') as f:
        fin = f.readlines()
        for line in fin:
            if line[:2] == matrix_type_1:
                calib_matrix_1 = np.array(line[4:].strip().split(" ")).astype('float32').reshape(3,-1)
            elif line[:2] == matrix_type_2:
                calib_matrix_2 = np.array(line[4:].strip().split(" ")).astype('float32').reshape(3,-1)

    #Calculate depth-to-disparity
    cam1 = calib_matrix_1[:,:3] # left image - P2
    cam2 = calib_matrix_2[:,:3] # right image - P3

    Tmat = np.array([0.54, 0., 0.])

    rev_proj_matrix = np.zeros((4,4))

    cv2.stereoRectify(cameraMatrix1 = cam1,cameraMatrix2 = cam2, \
                    distCoeffs1 = 0, distCoeffs2 = 0, \
                    imageSize = image1_colored.shape[:2], \
                    R = np.identity(3), T = Tmat, \
                    R1 = None, R2 = None, \
                    P1 =  None, P2 =  None, Q = rev_proj_matrix)

    #Project disparity map onto 3D Point Cloud
    points = cv2.reprojectImageTo3D(disparity_result, rev_proj_matrix)

    #reflect on x axis
    reflect_matrix = np.identity(3)
    reflect_matrix[0] *= -1
    points = np.matmul(points,reflect_matrix)

    #extract colors from image
    colors = cv2.cvtColor(image1_colored, cv2.COLOR_BGR2RGB)

    #filter by min disparity
    mask = disparity_result > disparity_result.min()
    out_points = points[mask]
    out_colors = colors[mask]

    #filter by dimension
    idx = np.fabs(out_points[:,0]) < 4.5
    out_points = out_points[idx]
    out_colors = out_colors.reshape(-1, 3)
    out_colors = out_colors[idx]

    #Output the result 3D Point Cloud
    write_ply(result_dir, out_points, out_colors)
    print('%s saved' % 'sample_3d_pointcloud.ply')