import sqlite3
import os
from datetime import datetime


def connect_database(db_path):
    """连接现有的 SQLite 数据库"""
    return sqlite3.connect(db_path)


def insert_sensor(conn, sensor_type, sensor_name):
    """插入传感器信息"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor (sensor_type, sensor_name) VALUES (?, ?)",
        (sensor_type, sensor_name)
    )
    conn.commit()
    return cursor.lastrowid


def insert_sensor_calibration(conn, sensor_id, reference_frame, self_coords, translation, rotation):
    """插入传感器标定信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sensor_calibration (sensor_id, calibration_reference_frame, self_coordinates, 
           translation_parameters, rotation_parameters) 
           VALUES (?, ?, ?, ?, ?)""",
        (sensor_id, reference_frame, self_coords, translation, rotation)
    )
    conn.commit()
    return cursor.lastrowid


def insert_log_info(conn, log_name, log_date, map_id, vehicle_id, sensor_calibration_id):
    """插入日志信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO log_info (log_name, log_date, map_id, vehicle_id, sensor_calibration_id)
           VALUES (?, ?, ?, ?, ?)""",
        (log_name, log_date, map_id, vehicle_id, sensor_calibration_id)
    )
    conn.commit()
    return cursor.lastrowid


def insert_scene_info(conn, scene_description, log_info_id):
    """插入场景信息"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scene_info (scene_description, log_info_id, sample_count) VALUES (?, ?, 0)",
        (scene_description, log_info_id)
    )
    conn.commit()
    return cursor.lastrowid


def update_scene_info_sample(conn, scene_id, first_sample_id=None, last_sample_id=None, increment_count=False):
    """更新场景信息中的样本数量和首尾样本 ID"""
    cursor = conn.cursor()
    if increment_count:
        cursor.execute(
            "UPDATE scene_info SET sample_count = sample_count + 1 WHERE scene_id = ?",
            (scene_id,)
        )
    if first_sample_id is not None:
        cursor.execute(
            "UPDATE scene_info SET first_sample_id = ? WHERE scene_id = ?",
            (first_sample_id, scene_id)
        )
    if last_sample_id is not None:
        cursor.execute(
            "UPDATE scene_info SET last_sample_id = ? WHERE scene_id = ?",
            (last_sample_id, scene_id)
        )
    conn.commit()


def insert_sensor_data(conn, timestamp, calibration_id, file_format, image_blob, prev_data_id=None):
    """插入传感器数据（图像为 BLOB）"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sensor_data (timestamp, sensor_calibration_id, data_file_format, image_resolution, 
           previous_sensor_data_id) VALUES (?, ?, ?, ?, ?)""",
        (timestamp, calibration_id, file_format, image_blob, prev_data_id)
    )
    conn.commit()
    return cursor.lastrowid


def insert_sample_info(conn, timestamp, scene_id, sensor_data_id, prev_sample_id=None):
    """插入样本信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sample_info (timestamp, scene_id, sensor_data_id, previous_sample_id)
           VALUES (?, ?, ?, ?)""",
        (timestamp, scene_id, sensor_data_id, prev_sample_id)
    )
    conn.commit()
    return cursor.lastrowid


def insert_sample_annotation(conn, sample_id, category_description_id, bbox_center, bbox_size, coord, prev_annotation_id=None):
    """插入样本标注信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sample_annotation (sample_id, category_description_id, bbox_center_position, bbox_size, 
        coordinates, previous_annotation_id) VALUES (?, ?, ?, ?, ?, ?)""",
        (sample_id, category_description_id, bbox_center, bbox_size, coord, prev_annotation_id)
    )
    conn.commit()
    return cursor.lastrowid


def update_next_sensor_data_id(conn, current_id, prev_id):
    """更新前一个传感器数据的 next_sensor_data_id"""
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sensor_data SET next_sensor_data_id = ? WHERE sensor_data_id = ?",
            (current_id, prev_id)
        )
        conn.commit()


def update_next_sample_id(conn, current_id, prev_id):
    """更新前一个样本的 next_sample_id"""
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sample_info SET next_sample_id = ? WHERE sample_id = ?",
            (current_id, prev_id)
        )
        conn.commit()


def update_next_annotation_id(conn, current_id, prev_id):
    """更新前一个标注的 next_annotation_id"""
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sample_annotation SET next_annotation_id = ? WHERE annotation_id = ?",
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
            bbox_center = f"{parts[11]}, {parts[12]}, {parts[13]}"
            bbox_size = f"{parts[8]}, {parts[9]}, {parts[10]}"
            coord = f"{parts[4]}, {parts[5]}, {parts[6]}, {parts[7]}"
            annotations.append((category, bbox_center, bbox_size, coord))
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
        "SELECT category_description_id FROM category_description WHERE category_subcategory_name = ?",
        (category_name,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO category_description (category_subcategory_name) VALUES (?)",
            (category_name,)
        )
        conn.commit()
        return cursor.lastrowid


def process_kitti_training_data(kitti_root, conn):
    """处理 KITTI 训练集并插入数据库"""
    camera_id = insert_sensor(conn, "Camera", "KITTI Camera")
    calibration_id = insert_sensor_calibration(conn, camera_id, "Camera Frame", "0,0,0", "0,0,0", "0,0,0")
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
        prev_annotation_id = None
        for category, bbox_center, bbox_size, coord in annotations:
            category_description_id = get_category_description_id(conn, category)
            annotation_id = insert_sample_annotation(conn, sample_id, category_description_id, bbox_center, bbox_size, coord, prev_annotation_id)
            update_next_annotation_id(conn, annotation_id, prev_annotation_id)
            prev_annotation_id = annotation_id


def process_kitti_test_data(kitti_root, conn):
    """处理 KITTI 测试集并插入数据库"""
    camera_id = insert_sensor(conn, "Camera", "KITTI Camera")
    calibration_id = insert_sensor_calibration(conn, camera_id, "Camera Frame", "0,0,0", "0,0,0", "0,0,0")
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


def process_kitti_data(kitti_root, db_path):
    """主函数：处理 KITTI 数据集并插入数据库"""
    conn = connect_database(db_path)

    # 处理训练集
    process_kitti_training_data(kitti_root, conn)

    # 处理测试集
    process_kitti_test_data(kitti_root, conn)

    print("训练集和测试集数据插入完成")
    conn.close()


if __name__ == "__main__":
    kitti_root = "E:\\kitti\\mini_kitti"
    db_path = r"E:\Tongji\Junior1\软件工程课程设计\test_database_2.db"
    process_kitti_data(kitti_root, db_path)
