from sqlite3 import connect
from turtle import update
import mysql.connector
import os
import posixpath
from datetime import datetime

local_connection = mysql.connector.connect(
    host="localhost",
    user="root",  # 替换为你的 MySQL 用户名
    password="root",  # 替换为你的 MySQL 密码
    database="car_perception_db"  # 替换为你的 MySQL 数据库名
)

remote_connection = mysql.connector.connect(
    host="122.51.133.37",
    user="dev",  # 替换为你的 MySQL 用户名
    password="dev123",  # 替换为你的 MySQL 密码
    database="car_perception_db"  # 替换为你的 MySQL 数据库名
)  

def connect_database():
    """连接本地 MySQL 数据库"""
    return local_connection

def insert_sensor(conn, sensor_type, sensor_name):
    """插入传感器信息"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor (sensor_type, sensor_name) VALUES (%s, %s)",
        (sensor_type, sensor_name)
    )
    conn.commit()
    return cursor.lastrowid

def insert_map_info(conn, location, filename, version, category):
    """插入地图信息"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO map_info (location, filename, version, category) VALUES (%s, %s, %s, %s)",
        (location, filename, version, category)
    )
    conn.commit()
    return cursor.lastrowid

def add_log_info(conn, log_name, log_date, map_id, vehicle_id):
    """插入日志信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO log_info (log_name, log_date, map_id, vehicle_id)
           VALUES (%s, %s, %s, %s)""",
        (log_name, log_date, map_id, vehicle_id)
    )
    conn.commit()
    return cursor.lastrowid

def add_scene_info(conn, scene_description, log_info_id):
    """插入场景信息"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scene_info (scene_description, log_info_id, sample_count) VALUES (%s, %s, 0)",
        (scene_description, log_info_id)
    )
    conn.commit()
    return cursor.lastrowid

def update_scene_info_sample(conn, scene_id, first_sample_id=None, last_sample_id=None, increment_count=False):
    """更新场景信息中的样本数量和首尾样本 ID"""
    cursor = conn.cursor()
    if increment_count:
        cursor.execute(
            "UPDATE scene_info SET sample_count = sample_count + 1 WHERE scene_id = %s",
            (scene_id,)
        )
    if first_sample_id is not None:
        cursor.execute(
            "UPDATE scene_info SET first_sample_id = %s WHERE scene_id = %s",
            (first_sample_id, scene_id)
        )
    if last_sample_id is not None:
        cursor.execute(
            "UPDATE scene_info SET last_sample_id = %s WHERE scene_id = %s",
            (last_sample_id, scene_id)
        )
    conn.commit()

def insert_sensor_calibration(conn, calibration_data, sensor_id):
    """将标定数据插入数据库，如果已经存在相同的数据则返回已有的ID"""
    cursor = conn.cursor()
    
    # 检查是否存在相同的标定数据
    cursor.execute(
        """
        SELECT sensor_calibration_id FROM sensor_calibration WHERE
        sensor_id = %s AND
        self_coordinates_x = %s AND self_coordinates_y = %s AND self_coordinates_z = %s AND
        translation_x = %s AND translation_y = %s AND translation_z = %s AND
        rotation_qw = %s AND rotation_qx = %s AND rotation_qy = %s AND rotation_qz = %s AND
        focal_length_x = %s AND focal_length_y = %s AND
        principal_point_x = %s AND principal_point_y = %s AND
        radial_distortion_k1 = %s AND radial_distortion_k2 = %s AND radial_distortion_k3 = %s AND
        tangential_distortion_p1 = %s AND tangential_distortion_p2 = %s
        """,
        (
            sensor_id,
            calibration_data.get('self_coordinates_x', None),
            calibration_data.get('self_coordinates_y', None),
            calibration_data.get('self_coordinates_z', None),
            calibration_data.get('translation_x', None),
            calibration_data.get('translation_y', None),
            calibration_data.get('translation_z', None),
            calibration_data.get('rotation_qw', None),
            calibration_data.get('rotation_qx', None),
            calibration_data.get('rotation_qy', None),
            calibration_data.get('rotation_qz', None),
            calibration_data.get('focal_length_x', None),
            calibration_data.get('focal_length_y', None),
            calibration_data.get('principal_point_x', None),
            calibration_data.get('principal_point_y', None),
            calibration_data.get('radial_distortion_k1', None),
            calibration_data.get('radial_distortion_k2', None),
            calibration_data.get('radial_distortion_k3', None),
            calibration_data.get('tangential_distortion_p1', None),
            calibration_data.get('tangential_distortion_p2', None)
        )
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # 如果没有找到相同的数据，则插入新数据
    cursor.execute(
        """
        INSERT INTO sensor_calibration (
            sensor_id, self_coordinates_x, self_coordinates_y, self_coordinates_z,
            translation_x, translation_y, translation_z, rotation_qw, rotation_qx,
            rotation_qy, rotation_qz, focal_length_x, focal_length_y, principal_point_x,
            principal_point_y, radial_distortion_k1, radial_distortion_k2, radial_distortion_k3,
            tangential_distortion_p1, tangential_distortion_p2
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            sensor_id,
            calibration_data.get('self_coordinates_x', None),
            calibration_data.get('self_coordinates_y', None),
            calibration_data.get('self_coordinates_z', None),
            calibration_data.get('translation_x', None),
            calibration_data.get('translation_y', None),
            calibration_data.get('translation_z', None),
            calibration_data.get('rotation_qw', None),
            calibration_data.get('rotation_qx', None),
            calibration_data.get('rotation_qy', None),
            calibration_data.get('rotation_qz', None),
            calibration_data.get('focal_length_x', None),
            calibration_data.get('focal_length_y', None),
            calibration_data.get('principal_point_x', None),
            calibration_data.get('principal_point_y', None),
            calibration_data.get('radial_distortion_k1', None),
            calibration_data.get('radial_distortion_k2', None),
            calibration_data.get('radial_distortion_k3', None),
            calibration_data.get('tangential_distortion_p1', None),
            calibration_data.get('tangential_distortion_p2', None)
        )
    )
    conn.commit()
    return cursor.lastrowid

def add_sensor_data(conn, timestamp, sensor_calibration_id, data_file_format, file_path,
                      previous_sensor_data_id=None, next_sensor_data_id=None, image_width=None,
                      image_height=None, is_key_frame=0, ego_translation_x=None,
                      ego_translation_y=None, ego_translation_z=None, ego_rotation_qw=None,
                      ego_rotation_qx=None, ego_rotation_qy=None, sample_id=None,
                      ego_rotation_qz=None):
    """插入传感器数据"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sensor_data (
            timestamp, sensor_calibration_id, data_file_format, file_path,
            previous_sensor_data_id, next_sensor_data_id, image_width,
            image_height, is_key_frame, ego_translation_x, ego_translation_y,
            ego_translation_z, ego_rotation_qw, ego_rotation_qx,
            ego_rotation_qy, sample_id, ego_rotation_qz
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (timestamp, sensor_calibration_id, data_file_format, file_path,
         previous_sensor_data_id, next_sensor_data_id, image_width,
         image_height, is_key_frame, ego_translation_x, ego_translation_y,
         ego_translation_z, ego_rotation_qw, ego_rotation_qx,
         ego_rotation_qy, sample_id, ego_rotation_qz)
    )
    conn.commit()
    return cursor.lastrowid

def add_sample_info(conn, timestamp, scene_id=None, previous_sample_id=None, next_sample_id=None):
    """插入样本信息"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sample_info (
            timestamp, scene_id, previous_sample_id, next_sample_id
        ) VALUES (%s, %s, %s, %s)
        """,
        (timestamp, scene_id, previous_sample_id, next_sample_id)
    )
    conn.commit()
    return cursor.lastrowid

def add_sample_annotation(conn, sample_id, bbox_center_3d_x=None, bbox_center_3d_y=None, bbox_center_3d_z=None,
                             bbox_3d_width_y=None, bbox_3d_height_z=None, bbox_3d_length_x=None,
                             previous_annotation_id=None, next_annotation_id=None,
                             num_lidar_pts=0, num_radar_pts=0, rotation_qw=None, rotation_qx=None,
                             rotation_qy=None, rotation_qz=None, instance_id=None):
    """插入样本注释"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sample_annotation (
            sample_id, bbox_center_3d_x, bbox_center_3d_y, bbox_center_3d_z,
            bbox_3d_width_y, bbox_3d_height_z, bbox_3d_length_x, previous_annotation_id,
            next_annotation_id, num_lidar_pts, num_radar_pts, rotation_qw, rotation_qx,
            rotation_qy, rotation_qz, instance_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (sample_id, bbox_center_3d_x, bbox_center_3d_y, bbox_center_3d_z,
         bbox_3d_width_y, bbox_3d_height_z, bbox_3d_length_x, previous_annotation_id,
         next_annotation_id, num_lidar_pts, num_radar_pts, rotation_qw, rotation_qx,
         rotation_qy, rotation_qz, instance_id)
    )
    conn.commit()
    return cursor.lastrowid

def add_annotation_2d(conn, bbox_2d_xmin=None, bbox_2d_xmax=None, bbox_2d_ymin=None, 
                        bbox_2d_ymax=None, sample_annotation_id=None, sensor_data_id=None):
    """插入2D标注信息"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO annotation_2d (
            bbox_2d_xmin, bbox_2d_xmax, bbox_2d_ymin, bbox_2d_ymax,
            sample_annotation_id, sensor_data_id
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (bbox_2d_xmin, bbox_2d_xmax, bbox_2d_ymin, bbox_2d_ymax,
            sample_annotation_id, sensor_data_id)
    )
    conn.commit()
    return cursor.lastrowid

def get_or_add_instance(conn, category_description_id, instance_count=0, first_annotation_id=None, last_annotation_id=None):
    """根据类别ID插入或返回实例信息"""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT instance_id FROM instance WHERE category_description_id = %s
        """,
        (category_description_id,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            """
            INSERT INTO instance (
                category_description_id, instance_count, first_annotation_id, last_annotation_id
            ) VALUES (%s, %s, %s, %s)
            """,
            (category_description_id, instance_count, first_annotation_id, last_annotation_id)
        )
        conn.commit()
        return cursor.lastrowid

def get_or_add_category_description(conn, category_subcategory_name, category_description=None):
    """根据类别信息检查并插入或返回类别描述信息"""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT category_description_id FROM category_description WHERE category_subcategory_name = %s
        """,
        (category_subcategory_name,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            """
            INSERT INTO category_description (
                category_subcategory_name, category_description
            ) VALUES (%s, %s)
            """,
            (category_subcategory_name, category_description)
        )
        conn.commit()
        return cursor.lastrowid

def add_attribute(conn, attribute_name, attribute_value, attribute_description=None):
    """插入属性信息"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO attribute (
            attribute_name, attribute_value, attribute_description
        ) VALUES (%s, %s, %s)
        """,
        (attribute_name, attribute_value, attribute_description)
    )
    conn.commit()
    return cursor.lastrowid

def add_annotation_attribute(conn, annotation_id, attribute_id):
    """插入注释属性信息"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO annotation_attribute (
            annotation_id, attribute_id
        ) VALUES (%s, %s)
        """,
        (annotation_id, attribute_id)
    )
    conn.commit()


def update_next_sensor_data_id(conn, current_id, prev_id):
    """更新前一个传感器数据的 next_sensor_data_id"""
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sensor_data SET next_sensor_data_id = %s WHERE sensor_data_id = %s",
            (current_id, prev_id)
        )
        conn.commit()

def update_next_sample_id(conn, current_id, prev_id):
    """更新前一个样本的 next_sample_id"""
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sample_info SET next_sample_id = %s WHERE sample_id = %s",
            (current_id, prev_id)
        )
        conn.commit()

def update_next_annotation_id(conn, current_id, prev_id):
    """更新前一个标注的 next_annotation_id"""
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sample_annotation SET next_annotation_id = %s WHERE annotation_id = %s",
            (current_id, prev_id)
        )
        conn.commit()

def read_image_as_blob(image_path):
    """将图像读取为 BLOB"""
    with open(image_path, 'rb') as f:
        return f.read()

def parse_label_file(label_path):
    """解析标注文件"""
    annotations = []
    with open(label_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            category = parts[0]
            bbox_center = (float(parts[11]), float(parts[12]), float(parts[13]))
            bbox_size = (float(parts[8]), float(parts[9]), float(parts[10]))
            bbox_2d = (float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7]))
            annotations.append((category, bbox_center, bbox_size, bbox_2d))
    return annotations

def parse_kitti_directory(root_path, dataset_type):
    """解析 KITTI 数据集的目录结构"""
    data = {"images": [], "labels": [] if dataset_type == "training" else None, "calib": [], "lidar": []}
    
    image_folder = "kitti_mini_data_object_image_2"
    label_folder = "kitti_mini_data_object_label_2"
    calib_folder = "kitti_mini_data_object_calib"
    lidar_folder = "kitti_mini_data_object_veloyne"

    if dataset_type == "training":
        base_image_path = posixpath.join(root_path, image_folder, "training")
        base_label_path = posixpath.join(root_path, label_folder, "training")
        base_calib_path = posixpath.join(root_path, calib_folder, "training")
        base_lidar_path = posixpath.join(root_path, lidar_folder, "training")
    elif dataset_type == "testing":
        base_image_path = posixpath.join(root_path, image_folder, "testing")
        base_calib_path = posixpath.join(root_path, calib_folder, "testing")
        base_lidar_path = posixpath.join(root_path, lidar_folder, "testing")
    else:
        raise ValueError("Invalid dataset type. Must be 'training' or 'testing'")

    # 解析图像数据
    for root, _, files in os.walk(base_image_path):
        for file in sorted(files):
            root = root.replace("\\", "/")
            if file.endswith(".png"):
                data["images"].append(posixpath.join(root, file))

    # 解析标签数据（仅训练集有标签）
    if dataset_type == "training":
        for root, _, files in os.walk(base_label_path):
            root = root.replace("\\", "/")
            for file in sorted(files):
                if file.endswith(".txt"):
                    data["labels"].append(posixpath.join(root, file))
    
    # 解析标定数据
    for root, _, files in os.walk(base_calib_path):
        root = root.replace("\\", "/")
        for file in sorted(files):
            if file.endswith(".txt"):
                data["calib"].append(posixpath.join(root, file))

    # 解析LiDAR数据
    for root, _, files in os.walk(base_lidar_path):
        root = root.replace("\\", "/")
        for file in sorted(files):
            if file.endswith(".bin"):
                data["lidar"].append(posixpath.join(root, file))

    return data


def parse_calibration_file(calib_path):
    """解析 KITTI 标定文件内容并转换为 sensor_calibration 表所需格式"""
    calibration_data = {}
    current_key = None
    current_value = []

    with open(calib_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            line = line.strip()

            # 如果包含冒号，则表示新的一行键值对
            if ':' in line:
                if current_key:
                    # 如果已经有一个正在收集的键值对，保存到数据字典中
                    calibration_data[current_key] = [float(v) for v in " ".join(current_value).split()]
                
                # 解析新的键和值
                try:
                    current_key, value = line.split(':', 1)
                    current_value = [value.strip()]  # 初始化当前值列表
                except ValueError:
                    print(f"无法解析的行: {line}")
                    current_key = None
                    current_value = []
            else:
                # 如果是上一个键的延续部分，将这一行加入当前值列表
                if current_key:
                    current_value.append(line)
        
        # 处理最后一个键值对
        if current_key:
            calibration_data[current_key] = [float(v) for v in " ".join(current_value).split()]

    # 组织标定数据到期望格式
    parsed_data = {}
    for key, values in calibration_data.items():
        if key in ['P0', 'P1', 'P2', 'P3']:
            parsed_data[key] = {
                'focal_length_x': values[0],
                'focal_length_y': values[5],
                'principal_point_x': values[2],
                'principal_point_y': values[6]
            }
        elif key == 'R0_rect':
            parsed_data['rotation_roll'] = values[0]
            parsed_data['rotation_pitch'] = values[1]
            parsed_data['rotation_yaw'] = values[2]
        elif key == 'Tr_velo_to_cam':
            parsed_data['translation_x'] = values[3]
            parsed_data['translation_y'] = values[7]
            parsed_data['translation_z'] = values[11]
        elif key == 'Tr_imu_to_velo':
            parsed_data['self_coordinates_x'] = values[3]
            parsed_data['self_coordinates_y'] = values[7]
            parsed_data['self_coordinates_z'] = values[11]

    return parsed_data



def process_kitti_training_data(kitti_root, conn):
    """处理 KITTI 训练集并插入数据库"""
    kitti_data = parse_kitti_directory(kitti_root, "training")

    print(f"训练集图像数量: {len(kitti_data['images'])}")
    print(f"训练集标签数量: {len(kitti_data['labels'])}")
    print(f"训练集标定数量: {len(kitti_data['calib'])}")
    print(f"训练集LiDAR数量: {len(kitti_data['lidar'])}")
    
    # 插入地图、传感器和日志信息
    map_id = insert_map_info(conn, "KITTI Area", "kitti_map.osm", "1.0", "urban")
    
    # 插入不同类型的传感器
    sensor_camera_id = insert_sensor(conn, "camera", "KITTI Camera")
    sensor_lidar_id = insert_sensor(conn, "lidar", "KITTI LiDAR")
    log_id = add_log_info(conn, "KITTI Training Log", datetime.now(), map_id, "Vehicle_001")
    
    # 插入场景信息
    scene_id = add_scene_info(conn, "KITTI Training Data Scene", log_id)
    
    first_sample_id = None
    previous_sample_id = None
    previous_sensor_data_ids = {}
    previous_annotation_id = None
    
    # 处理每一帧数据，按照时间戳顺序插入
    for idx, image_path in enumerate(kitti_data["images"]):
        timestamp = datetime.now()  # 使用当前时间作为时间戳
        
        # 插入标定数据
        calib_path = kitti_data["calib"][idx]
        calibration_data = parse_calibration_file(calib_path)
        sensor_calibration_id_camera = insert_sensor_calibration(conn, calibration_data, sensor_camera_id)
        sensor_calibration_id_lidar = insert_sensor_calibration(conn, calibration_data, sensor_lidar_id)
        
        # 插入样本信息
        sample_id = add_sample_info(conn, timestamp, scene_id, previous_sample_id, None)
        if previous_sample_id:
            update_next_sample_id(conn, sample_id, previous_sample_id)
        previous_sample_id = sample_id
        if not first_sample_id:
            first_sample_id = sample_id

        update_scene_info_sample(conn, scene_id, first_sample_id, sample_id, increment_count=True)
        
        # 插入相机传感器数据（图像）
        sensor_data_id = add_sensor_data(
            conn, timestamp, sensor_calibration_id_camera, "png", image_path,
            previous_sensor_data_ids.get("image"), None, image_width=None,
            image_height=None, is_key_frame=1, ego_translation_x=None,
            ego_translation_y=None, ego_translation_z=None, ego_rotation_qw=None,
            ego_rotation_qx=None, ego_rotation_qy=None, sample_id=sample_id,
            ego_rotation_qz=None
        )
        if previous_sensor_data_ids.get("image"):
            update_next_sensor_data_id(conn, sensor_data_id, previous_sensor_data_ids.get("image"))
        previous_sensor_data_ids["image"] = sensor_data_id
        
        # 插入LiDAR传感器数据
        lidar_path = kitti_data["lidar"][idx]
        # 插入LiDAR传感器数据
        lidar_data_id = add_sensor_data(
            conn, timestamp, sensor_calibration_id_lidar, "bin", lidar_path,
            previous_sensor_data_ids.get("lidar"), None, None, None, 0, None, None, None, None, None, None, sample_id, None
        )
        if previous_sensor_data_ids.get("lidar"):
            update_next_sensor_data_id(conn, lidar_data_id, previous_sensor_data_ids.get("lidar"))
        previous_sensor_data_ids["lidar"] = lidar_data_id

        # 插入标注信息
        label_path = kitti_data["labels"][idx]
        annotations = parse_label_file(label_path)
        
        for annotation in annotations:
            category_name, bbox_center, bbox_size, bbox_2d = annotation
            category_id = get_or_add_category_description(conn, category_name)
            instance_id = get_or_add_instance(conn, category_id)
            
            # Add 3D annotation
            annotation_id = add_sample_annotation(
                conn, sample_id, 
                bbox_center_3d_x=bbox_center[0], 
                bbox_center_3d_y=bbox_center[1], 
                bbox_center_3d_z=bbox_center[2],
                bbox_3d_width_y=bbox_size[1], 
                bbox_3d_height_z=bbox_size[2], 
                bbox_3d_length_x=bbox_size[0],
                previous_annotation_id=previous_annotation_id,
                num_lidar_pts=0,
                num_radar_pts=0,
                instance_id=instance_id
            )

            # Add 2D annotation for this sensor data 
            add_annotation_2d(
                conn,
                bbox_2d_xmin=bbox_2d[0],
                bbox_2d_xmax=bbox_2d[2], 
                bbox_2d_ymin=bbox_2d[1],
                bbox_2d_ymax=bbox_2d[3],
                sample_annotation_id=annotation_id,
                sensor_data_id=sensor_data_id
            )
            if previous_annotation_id:
                update_next_annotation_id(conn, annotation_id, previous_annotation_id)
            previous_annotation_id = annotation_id
    
    print("训练集数据插入完成")

def process_kitti_testing_data(kitti_root, conn):
    """处理 KITTI 测试集并插入数据库"""
    kitti_data = parse_kitti_directory(kitti_root, "testing")
    
    # 插入地图、传感器和日志信息
    map_id = insert_map_info(conn, "KITTI Area", "kitti_map.osm", "1.0", "urban")
    
    # 插入不同类型的传感器
    sensor_camera_id = insert_sensor(conn, "camera", "KITTI Camera")
    sensor_lidar_id = insert_sensor(conn, "lidar", "KITTI LiDAR")
    log_id = add_log_info(conn, "KITTI Testing Log", datetime.now(), map_id, "Vehicle_001")
    
    # 插入场景信息
    scene_id = add_scene_info(conn, "KITTI Testing Data Scene", log_id)
    
    first_sample_id = None
    previous_sample_id = None
    previous_sensor_data_ids = {}
    
    # 处理每一帧数据，按照时间戳顺序插入
    for idx, image_path in enumerate(kitti_data["images"]):
        timestamp = datetime.now()  # 使用当前时间作为时间戳
        
        # 插入标定数据
        calib_path = kitti_data["calib"][idx]
        calibration_data = parse_calibration_file(calib_path)
        sensor_calibration_id_camera = insert_sensor_calibration(conn, calibration_data, sensor_camera_id)
        sensor_calibration_id_lidar = insert_sensor_calibration(conn, calibration_data, sensor_lidar_id)
        
        # 插入样本信息
        sample_id = add_sample_info(conn, timestamp, scene_id, previous_sample_id, None)
        if previous_sample_id:
            update_next_sample_id(conn, sample_id, previous_sample_id)
        previous_sample_id = sample_id
        if not first_sample_id:
            first_sample_id = sample_id

        update_scene_info_sample(conn, scene_id, first_sample_id, sample_id, increment_count=True)
        
        # 插入相机传感器数据（图像）
        sensor_data_id = add_sensor_data(
            conn, timestamp, sensor_calibration_id_camera, "png", image_path,
            previous_sensor_data_ids.get("image"), None, None, None, 1, None, None, None, None, None, None, sample_id, None
        )
        if previous_sensor_data_ids.get("image"):
            update_next_sensor_data_id(conn, sensor_data_id, previous_sensor_data_ids.get("image"))
        previous_sensor_data_ids["image"] = sensor_data_id

        # 插入LiDAR传感器数据
        lidar_path = kitti_data["lidar"][idx]
        lidar_data_id = add_sensor_data(
            conn, timestamp, sensor_calibration_id_lidar, "bin", lidar_path,
            previous_sensor_data_ids.get("lidar"), None, None, None, 0, None, None, None, None, None, None, sample_id, None
        )
        if previous_sensor_data_ids.get("lidar"):
            update_next_sensor_data_id(conn, lidar_data_id, previous_sensor_data_ids.get("lidar"))
        previous_sensor_data_ids["lidar"] = lidar_data_id
    
    print("测试集数据插入完成")

def process_kitti_data(kitti_root):
    """主函数：处理 KITTI 数据集并插入数据库"""
    conn = connect_database()

    # 处理训练集
    process_kitti_training_data(kitti_root, conn)

    # 处理测试集
    process_kitti_testing_data(kitti_root, conn)

    conn.close()

if __name__ == "__main__":
    os.chdir("D:/datasets")
    kitti_root = "kitti/mini_kitti"
    process_kitti_data(kitti_root)
