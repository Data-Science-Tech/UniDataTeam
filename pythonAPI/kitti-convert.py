import sqlite3
import os
import xml.etree.ElementTree as ET
import glob

# 获取当前 Python 文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在的目录
current_directory = os.path.dirname(current_file_path)
print("当前目录:", current_directory)

relative_db_folder = r'../database'

db_folder = os.path.join(current_directory, relative_db_folder)
db_path = os.path.join(db_folder, 'test_database.db')
print("数据库路径:", os.path.abspath(db_path))

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# 连接SQLite数据库（如果数据库不存在，将自动创建）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# 假设你有一个KITTI数据集路径
kitti_dataset_path = r'D:\datasets\kitti\2011_09_26'

def insert_sensor(sensor_type, sensor_name):
    cursor.execute('''
        INSERT INTO sensor (sensor_type, sensor_name)
        VALUES (?, ?)
    ''', (sensor_type, sensor_name))
    return cursor.lastrowid

def insert_sensor_calibration(sensor_id, reference_frame, self_coordinates, translation_parameters, rotation_parameters):
    cursor.execute('''
        INSERT INTO sensor_calibration (sensor_id, calibration_reference_frame, self_coordinates, translation_parameters, rotation_parameters)
        VALUES (?, ?, ?, ?, ?)
    ''', (sensor_id, reference_frame, self_coordinates, translation_parameters, rotation_parameters))
    return cursor.lastrowid

def insert_map_info(map_type, is_rotated, coordinate_system_name):
    cursor.execute('''
        INSERT INTO map_info (map_type, is_rotated, coordinate_system_name)
        VALUES (?, ?, ?)
    ''', (map_type, is_rotated, coordinate_system_name))
    return cursor.lastrowid

def insert_log_info(log_name, log_date, map_id, vehicle_id, sensor_calibration_id):
    cursor.execute('''
        INSERT INTO log_info (log_name, log_date, map_id, vehicle_id, sensor_calibration_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (log_name, log_date, map_id, vehicle_id, sensor_calibration_id))
    return cursor.lastrowid

def insert_scene_info(scene_description, log_info_id):
    cursor.execute('''
        INSERT INTO scene_info (scene_description, log_info_id)
        VALUES (?, ?)
    ''', (scene_description, log_info_id))
    return cursor.lastrowid

def insert_sensor_data(timestamp, sensor_calibration_id, data_file_format, image_data, previous_sensor_data_id=None):
    cursor.execute('''
        INSERT INTO sensor_data (timestamp, sensor_calibration_id, data_file_format, image_resolution, previous_sensor_data_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, sensor_calibration_id, data_file_format, image_data, previous_sensor_data_id))
    sensor_data_id = cursor.lastrowid
    return sensor_data_id

def update_previous_sensor_data(previous_sensor_data_id, current_sensor_data_id):
    if previous_sensor_data_id:
        cursor.execute('''
            UPDATE sensor_data
            SET next_sensor_data_id = ?
            WHERE sensor_data_id = ?
        ''', (current_sensor_data_id, previous_sensor_data_id))

def insert_sample_info(timestamp, scene_id, sensor_data_id, previous_sample_id=None):
    cursor.execute('''
        INSERT INTO sample_info (timestamp, scene_id, sensor_data_id, previous_sample_id)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, scene_id, sensor_data_id, previous_sample_id))
    sample_id = cursor.lastrowid
    return sample_id

def update_previous_sample(previous_sample_id, current_sample_id):
    if previous_sample_id:
        cursor.execute('''
            UPDATE sample_info
            SET next_sample_id = ?
            WHERE sample_id = ?
        ''', (current_sample_id, previous_sample_id))

def insert_sample_annotation(sample_id, category_description_id, bbox_center_position, bbox_size):
    cursor.execute('''
        INSERT INTO sample_annotation (sample_id, category_description_id, bbox_center_position, bbox_size)
        VALUES (?, ?, ?, ?)
    ''', (sample_id, category_description_id, bbox_center_position, bbox_size))
    return cursor.lastrowid

def process_kitti_data():
    # 遍历KITTI数据集中的所有场景数据
    scene_folders = [folder for folder in os.listdir(kitti_dataset_path) if os.path.isdir(os.path.join(kitti_dataset_path, folder))]
    for scene_folder in scene_folders:
        scene_path = os.path.join(kitti_dataset_path, scene_folder)

        # 插入传感器信息（Camera和LiDAR）
        camera_sensor_id = insert_sensor('Camera', 'KITTI Camera')
        lidar_sensor_id = insert_sensor('LiDAR', 'KITTI LiDAR')

        # 读取并插入传感器校准信息
        calib_files = ['calib_cam_to_cam.txt', 'calib_imu_to_velo.txt', 'calib_velo_to_cam.txt']
        for calib_file in calib_files:
            calib_path = os.path.join(scene_path, calib_file)
            if os.path.exists(calib_path):
                with open(calib_path, 'r') as f:
                    calibration_data = f.read()
                    # 这里假设所有校准文件使用相同的参考系、自身坐标，简化处理
                    insert_sensor_calibration(camera_sensor_id, 'Vehicle frame', 'Self coordinates', calibration_data, calibration_data)
                    insert_sensor_calibration(lidar_sensor_id, 'Vehicle frame', 'Self coordinates', calibration_data, calibration_data)

        # 插入地图信息
        map_id = insert_map_info('intersection', 0, 'WGS84')

        # 插入日志信息
        log_name = f'{scene_folder}_KITTI_log'
        log_date = scene_folder.split('_')[0]  # 假设场景名称包含日期信息
        log_info_id = insert_log_info(log_name, log_date, map_id, 1, camera_sensor_id)

        # 插入场景信息
        scene_description = f'Scene for {scene_folder}'
        scene_id = insert_scene_info(scene_description, log_info_id)

        previous_sample_id = None
        previous_lidar_data_id = None
        previous_camera_data_id = None

        # 读取并插入点云数据和时间戳信息
        velodyne_folder = os.path.join(scene_path, 'velodyne_points')
        if os.path.exists(velodyne_folder):
            timestamps_file = os.path.join(velodyne_folder, 'timestamps.txt')
            if os.path.exists(timestamps_file):
                with open(timestamps_file, 'r') as f:
                    timestamps = f.readlines()

                data_folder = os.path.join(velodyne_folder, 'data')
                if os.path.exists(data_folder):
                    for idx, timestamp in enumerate(timestamps):
                        timestamp = timestamp.strip()  # 转换时间戳格式
                        bin_file = os.path.join(data_folder, f'{idx:010d}.bin')
                        if os.path.exists(bin_file):
                            with open(bin_file, 'rb') as lidar_file:
                                lidar_data = lidar_file.read()
                            sensor_data_id = insert_sensor_data(timestamp, lidar_sensor_id, 'bin', lidar_data, previous_lidar_data_id)
                            update_previous_sensor_data(previous_lidar_data_id, sensor_data_id)
                            previous_lidar_data_id = sensor_data_id
                            sample_id = insert_sample_info(timestamp, scene_id, sensor_data_id, previous_sample_id)
                            update_previous_sample(previous_sample_id, sample_id)
                            previous_sample_id = sample_id

        # 读取并插入图像数据
        for image_index in range(4):  # image_00, image_01, image_02, image_03
            image_folder = os.path.join(scene_path, f'image_{image_index:02d}')
            if os.path.exists(image_folder):
                timestamp_file = os.path.join(image_folder, 'timestamps.txt')
                data_folder = os.path.join(image_folder, 'data')

                if os.path.exists(timestamp_file) and os.path.exists(data_folder):
                    # 读取时间戳文件
                    with open(timestamp_file, 'r') as f:
                        timestamps = f.readlines()

                    # 读取图像数据
                    for idx, timestamp in enumerate(timestamps):
                        timestamp = timestamp.strip()  # 将时间戳转换为标准格式（假设格式为"YYYY-MM-DD HH:MM:SS.ssssss"）
                        image_file = os.path.join(data_folder, f'{idx:010d}.png')
                        if os.path.exists(image_file):
                            with open(image_file, 'rb') as img_file:
                                image_data = img_file.read()
                            sensor_data_id = insert_sensor_data(timestamp, camera_sensor_id, 'png', image_data, previous_camera_data_id)
                            update_previous_sensor_data(previous_camera_data_id, sensor_data_id)
                            previous_camera_data_id = sensor_data_id
                            sample_id = insert_sample_info(timestamp, scene_id, sensor_data_id, previous_sample_id)
                            update_previous_sample(previous_sample_id, sample_id)
                            previous_sample_id = sample_id

    # 提交事务
    conn.commit()
    print("成功处理并插入了所有KITTI数据集的内容。")

# 执行处理
process_kitti_data()

# 关闭连接
conn.close()
print("数据库连接已关闭。")
