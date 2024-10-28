import mysql.connector
import os
from datetime import datetime

def connect_database():
    """连接本地 MySQL 数据库"""
    return mysql.connector.connect(
        host="localhost",
        user="root",  # 替换为你的 MySQL 用户名
        password="root",  # 替换为你的 MySQL 密码
        database="car_perception_db"  # 替换为你的 MySQL 数据库名
    )

def insert_sensor(conn, sensor_type, sensor_name):
    """插入传感器信息"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor (sensor_type, sensor_name) VALUES (%s, %s)",
        (sensor_type, sensor_name)
    )
    conn.commit()
    return cursor.lastrowid

def insert_sensor_calibration(conn, sensor_id, reference_frame, self_coords, translation, rotation):
    """插入传感器标定信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sensor_calibration (sensor_id, calibration_reference, self_coordinates_x, self_coordinates_y, self_coordinates_z, 
           translation_x, translation_y, translation_z, rotation_roll, rotation_pitch, rotation_yaw) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (sensor_id, reference_frame, self_coords[0], self_coords[1], self_coords[2], translation[0], translation[1], translation[2], rotation[0], rotation[1], rotation[2])
    )
    conn.commit()
    return cursor.lastrowid

def insert_log_info(conn, log_name, log_date, map_id, vehicle_id, sensor_calibration_id):
    """插入日志信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO log_info (log_name, log_date, map_id, vehicle_id, sensor_calibration_id)
           VALUES (%s, %s, %s, %s, %s)""",
        (log_name, log_date, map_id, vehicle_id, sensor_calibration_id)
    )
    conn.commit()
    return cursor.lastrowid

def insert_scene_info(conn, scene_description, log_info_id):
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

def insert_sensor_data(conn, timestamp, calibration_id, file_format, image_blob, prev_data_id=None):
    """插入传感器数据（图像为 BLOB）"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sensor_data (timestamp, sensor_calibration_id, data_file_format, image_resolution, 
           previous_sensor_data_id) VALUES (%s, %s, %s, %s, %s)""",
        (timestamp, calibration_id, file_format, image_blob, prev_data_id)
    )
    conn.commit()
    return cursor.lastrowid

def insert_sample_info(conn, timestamp, scene_id, sensor_data_id, prev_sample_id=None):
    """插入样本信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sample_info (timestamp, scene_id, sensor_data_id, previous_sample_id)
           VALUES (%s, %s, %s, %s)""",
        (timestamp, scene_id, sensor_data_id, prev_sample_id)
    )
    conn.commit()
    return cursor.lastrowid

def insert_sample_annotation(conn, sample_id, category_description_id, bbox_center, bbox_size, bbox_2d, prev_annotation_id=None):
    """插入样本标注信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sample_annotation (sample_id, category_description_id, 
        bbox_center_position_x, bbox_center_position_y, bbox_center_position_z, 
        bbox_width, bbox_height, bbox_depth, 
        2d_box_xmin, 2d_box_ymin, 2d_box_xmax, 2d_box_ymax, 
        previous_annotation_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (sample_id, category_description_id, bbox_center[0], bbox_center[1], bbox_center[2], 
         bbox_size[0], bbox_size[1], bbox_size[2], 
         bbox_2d[0], bbox_2d[1], bbox_2d[2], bbox_2d[3], prev_annotation_id)
    )
    conn.commit()
    return cursor.lastrowid

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
    data = {"images": [], "labels": [] if dataset_type == "training" else None}
    image_folder = "kitti_mini_data_object_image_2"
    label_folder = "kitti_mini_data_object_label_2"

    if dataset_type == "training":
        base_image_path = os.path.join(root_path, image_folder, "training")
        base_label_path = os.path.join(root_path, label_folder, "training")
    elif dataset_type == "testing":
        base_image_path = os.path.join(root_path, image_folder, "testing")
    else:
        raise ValueError("Invalid dataset type. Must be 'training' or 'testing'")

    for root, _, files in os.walk(base_image_path):
        for file in files:
            if file.endswith(".png"):
                data["images"].append(os.path.join(root, file))

    if dataset_type == "training":
        for root, _, files in os.walk(base_label_path):
            for file in files:
                if file.endswith(".txt"):
                    data["labels"].append(os.path.join(root, file))

    return data

def get_category_description_id(conn, category_name):
    """检查类别是否已存在，若存在则返回其 ID，否则插入新的类别并返回其 ID"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category_description_id FROM category_description WHERE category_subcategory_name = %s",
        (category_name,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO category_description (category_subcategory_name) VALUES (%s)",
            (category_name,)
        )
        conn.commit()
        return cursor.lastrowid

def process_kitti_training_data(kitti_root, conn):
    """处理 KITTI 训练集并插入数据库"""
    camera_id = insert_sensor(conn, "Camera", "KITTI Camera")
    calibration_id = insert_sensor_calibration(conn, camera_id, "Camera Frame", (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    log_info_id = insert_log_info(conn, "KITTI Training Log", "2024-10-25", None, None, calibration_id)
    scene_id = insert_scene_info(conn, "Training Scene", log_info_id)

    kitti_data = parse_kitti_directory(kitti_root, "training")
    sample_ids = []
    prev_sensor_data_id = None
    prev_sample_id = None
    first_sample_id = None

    for image_path in kitti_data["images"]:
        image_blob = read_image_as_blob(image_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sensor_data_id = insert_sensor_data(conn, timestamp, calibration_id, "png", image_blob, prev_sensor_data_id)
        update_next_sensor_data_id(conn, sensor_data_id, prev_sensor_data_id)

        sample_id = insert_sample_info(conn, timestamp, scene_id, sensor_data_id, prev_sample_id)
        update_next_sample_id(conn, sample_id, prev_sample_id)

        if first_sample_id is None:
            first_sample_id = sample_id

        update_scene_info_sample(conn, scene_id, increment_count=True, last_sample_id=sample_id)

        sample_ids.append(sample_id)
        prev_sensor_data_id = sensor_data_id
        prev_sample_id = sample_id

    # 更新场景信息中的首样本 ID
    if first_sample_id is not None:
        update_scene_info_sample(conn, scene_id, first_sample_id=first_sample_id)

    for label_path, sample_id in zip(kitti_data["labels"], sample_ids):
        annotations = parse_label_file(label_path)
        # print("正在处理标注文件：", label_path)
        prev_annotation_id = None
        for category, bbox_center, bbox_size, bbox_2d in annotations:
            category_description_id = get_category_description_id(conn, category)
            annotation_id = insert_sample_annotation(conn, sample_id, category_description_id, bbox_center, bbox_size, bbox_2d, prev_annotation_id)
            update_next_annotation_id(conn, annotation_id, prev_annotation_id)
            prev_annotation_id = annotation_id

def process_kitti_test_data(kitti_root, conn):
    """处理 KITTI 测试集并插入数据库"""
    camera_id = insert_sensor(conn, "Camera", "KITTI Camera")
    calibration_id = insert_sensor_calibration(conn, camera_id, "Camera Frame", (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    log_info_id = insert_log_info(conn, "KITTI Test Log", "2024-10-25", None, None, calibration_id)
    scene_id = insert_scene_info(conn, "Test Scene", log_info_id)

    kitti_data = parse_kitti_directory(kitti_root, "testing")
    prev_sensor_data_id = None

    for image_path in kitti_data["images"]:
        image_blob = read_image_as_blob(image_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sensor_data_id = insert_sensor_data(conn, timestamp, calibration_id, "png", image_blob, prev_sensor_data_id)
        update_next_sensor_data_id(conn, sensor_data_id, prev_sensor_data_id)
        prev_sensor_data_id = sensor_data_id

def process_kitti_data(kitti_root):
    """主函数：处理 KITTI 数据集并插入数据库"""
    conn = connect_database()

    # 处理训练集
    process_kitti_training_data(kitti_root, conn)

    # 处理测试集
    process_kitti_test_data(kitti_root, conn)

    print("训练集和测试集数据插入完成")
    conn.close()

if __name__ == "__main__":
    kitti_root = "D:\datasets\kitti\mini_kitti"
    process_kitti_data(kitti_root)
