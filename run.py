import sys
import json

from src.main import generate_3d_pointcloud


def main(targets):

    test_config = json.load(open("config/config.json"))

    if 'test' in targets:
        
        generate_3d_pointcloud(test_config['left_image_dir'], test_config['right_image_dir'], test_config['num_disparities'], test_config['block_size'], test_config['calibration_file_dir'], test_config['result_dir'])

if __name__ == '__main__':

    targets = sys.argv[1:]
    main(targets)