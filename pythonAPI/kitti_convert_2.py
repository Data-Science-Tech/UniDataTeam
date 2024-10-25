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

def insert_category_description(conn, category_name):
    """插入类别描述并返回 ID"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO category_description (category_subcategory_name) VALUES (?)",
        (category_name,)
    )
    conn.commit()
    return cursor.lastrowid

def get_category_description_id(conn, category_name):
    """检查类别是否已存在，若存在则返回其 ID"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category_description_id FROM category_description WHERE category_subcategory_name = ?",
        (category_name,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    return insert_category_description(conn, category_name)

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
        "INSERT INTO scene_info (scene_description, log_info_id) VALUES (?, ?)",
        (scene_description, log_info_id)
    )
    conn.commit()
    return cursor.lastrowid

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

def insert_sample_annotation(conn, sample_id, category_description_id, bbox_center, bbox_size):
    """插入样本标注信息"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sample_annotation (sample_id, category_description_id, bbox_center_position, bbox_size)
           VALUES (?, ?, ?, ?)""",
        (sample_id, category_description_id, bbox_center, bbox_size)
    )
    conn.commit()

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
            annotations.append((category, bbox_center, bbox_size))
    return annotations

def parse_kitti_directory(root_path):
    """解析 KITTI 数据集的目录结构"""
    data = {"images": [], "labels": []}
    for root, _, files in os.walk(root_path):
        for file in files:
            if "image_2" in root and file.endswith(".png"):
                data["images"].append(os.path.join(root, file))
            elif "label_2" in root and file.endswith(".txt"):
                data["labels"].append(os.path.join(root, file))
    return data

def process_kitti_data(kitti_root, db_path):
    """主函数：处理 KITTI 数据集并插入数据库"""
    conn = connect_database(db_path)

    camera_id = insert_sensor(conn, "Camera", "KITTI Camera")
    calibration_id = insert_sensor_calibration(conn, camera_id, "Camera Frame", "0,0,0", "0,0,0", "0,0,0")
    log_info_id = insert_log_info(conn, "KITTI Log", "2024-10-25", None, None, calibration_id)
    scene_id = insert_scene_info(conn, "Sample Scene", log_info_id)

    kitti_data = parse_kitti_directory(kitti_root)
    sample_ids = []
    prev_sensor_data_id = None
    prev_sample_id = None

    for image_path in kitti_data["images"]:
        image_blob = read_image_as_blob(image_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sensor_data_id = insert_sensor_data(conn, timestamp, calibration_id, "png", image_blob, prev_sensor_data_id)
        update_next_sensor_data_id(conn, sensor_data_id, prev_sensor_data_id)

        sample_id = insert_sample_info(conn, timestamp, scene_id, sensor_data_id, prev_sample_id)
        update_next_sample_id(conn, sample_id, prev_sample_id)

        sample_ids.append(sample_id)
        prev_sensor_data_id = sensor_data_id
        prev_sample_id = sample_id

    for label_path, sample_id in zip(kitti_data["labels"], sample_ids):
        annotations = parse_label_file(label_path)
        prev_annotation_id = None
        for category, bbox_center, bbox_size in annotations:
            category_description_id = get_category_description_id(conn, category)
            annotation_id = insert_sample_annotation(conn, sample_id, category_description_id, bbox_center, bbox_size)
            update_next_annotation_id(conn, annotation_id, prev_annotation_id)
            prev_annotation_id = annotation_id

    print("数据插入完成")
    conn.close()

if __name__ == "__main__":
    kitti_root = "E:\\kitti\\mini_kitti"
    db_path = r"E:\Tongji\Junior1\软件工程课程设计\my_test.db"
    process_kitti_data(kitti_root, db_path)
