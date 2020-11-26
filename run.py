from src.camera_calibration import calibrate_camera
import json

calibrate_camera_config = json.load(open("config/camera_calibration_config.json"))
calibrate_camera(calibrate_camera_config['fps'], calibrate_camera_config['image'], calibrate_camera_config['result'])