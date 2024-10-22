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
kitti_dataset_path = 'path_to_kitti_data'

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

def insert_sensor_data(timestamp, sensor_calibration_id, data_file_format, image_resolution):
    cursor.execute('''
        INSERT INTO sensor_data (timestamp, sensor_calibration_id, data_file_format, image_resolution)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, sensor_calibration_id, data_file_format, image_resolution))
    return cursor.lastrowid

def insert_sample_info(timestamp, scene_id, sensor_data_id):
    cursor.execute('''
        INSERT INTO sample_info (timestamp, scene_id, sensor_data_id)
        VALUES (?, ?, ?)
    ''', (timestamp, scene_id, sensor_data_id))
    return cursor.lastrowid

def process_kitti_data():
    # 遍历KITTI数据集中的所有传感器数据
    # 插入传感器信息（Camera和LiDAR）
    camera_sensor_id = insert_sensor('Camera', 'KITTI Camera')
    lidar_sensor_id = insert_sensor('LiDAR', 'KITTI LiDAR')

    # 读取并插入传感器校准信息
    calib_files = ['calib_cam_to_cam.txt', 'calib_imu_to_velo.txt', 'calib_velo_to_cam.txt']
    for calib_file in calib_files:
        calib_path = os.path.join(kitti_dataset_path, calib_file)
        if os.path.exists(calib_path):
            with open(calib_path, 'r') as f:
                calibration_data = f.read()
                # 这里假设所有校准文件使用相同的参考系、自身坐标，简化处理
                insert_sensor_calibration(camera_sensor_id, 'Vehicle frame', 'Self coordinates', calibration_data, calibration_data)
                insert_sensor_calibration(lidar_sensor_id, 'Vehicle frame', 'Self coordinates', calibration_data, calibration_data)

    # 插入地图信息
    map_id = insert_map_info('intersection', 0, 'WGS84')

    # 插入日志信息
    log_info_id = insert_log_info('2024-01-01_KITTI_log', '2024-01-01', map_id, 1, camera_sensor_id)

    # 读取并插入点云数据和图片数据
    velodyne_folder = os.path.join(kitti_dataset_path, 'velodyne_points')

    if os.path.exists(velodyne_folder):
        for file in sorted(os.listdir(velodyne_folder)):
            if file.endswith('.bin'):
                timestamp = file.split('.')[0]  # 假设文件名包含时间戳
                sensor_data_id = insert_sensor_data(timestamp, lidar_sensor_id, 'bin', None)
                insert_sample_info(timestamp, None, sensor_data_id)

    # 读取并插入图像数据
    for image_index in range(4):  # image_00, image_01, image_02, image_03
        image_folder = os.path.join(kitti_dataset_path, f'image_{image_index:02d}')
        if os.path.exists(image_folder):
            timestamp_file = os.path.join(image_folder, 'timestamps.txt')
            data_folder = os.path.join(image_folder, 'data')

            if os.path.exists(timestamp_file) and os.path.exists(data_folder):
                # 读取时间戳文件
                with open(timestamp_file, 'r') as f:
                    timestamps = f.readlines()

                # 读取图像数据
                for idx, timestamp in enumerate(timestamps):
                    timestamp = timestamp.strip()
                    image_file = os.path.join(data_folder, f'{idx:010d}.png')
                    if os.path.exists(image_file):
                        sensor_data_id = insert_sensor_data(timestamp, camera_sensor_id, 'png', '1242x375')
                        insert_sample_info(timestamp, None, sensor_data_id)

    # 读取并插入标注信息
    tracklet_file = os.path.join(kitti_dataset_path, 'tracklet_labels.xml')
    if os.path.exists(tracklet_file):
        tree = ET.parse(tracklet_file)
        root = tree.getroot()
        for tracklet in root.findall('tracklet'):  # 根据tracklet标签
            object_type = tracklet.find('objectType').text
            first_frame = tracklet.find('first_frame').text
            # 可以进一步处理其他标注数据并插入数据库
            # 此处简化处理，仅插入类别描述
            insert_map_info(object_type, 0, 'WGS84')

    # 提交事务
    conn.commit()

# 执行处理
process_kitti_data()

# 关闭连接
conn.close()
