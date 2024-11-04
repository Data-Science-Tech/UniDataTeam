from nuscenes.nuscenes import NuScenes
import os
current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import mysql.connector
from mysql.connector import Error
import math
import datetime
nusc = NuScenes(version='v1.0-mini', dataroot = current_folder + '\\v1.0-mini', verbose = True)

def connect_database():
    """连接本地 MySQL 数据库"""
    return mysql.connector.connect(
        host='localhost',      
        port=3306,              
        user='root',            
        password='qin3398466884',  
        database='car_perception_db'  
    )

def insert_annotation_attribute(connection, annotation_id, attribute_id):
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO annotation_attribute (annotation_id, attribute_id)
    VALUES (%s, %s)
    """
    
    cursor.execute(insert_query, (annotation_id, attribute_id))
    connection.commit()
    cursor.close()

def insert_attribute(connection, attribute_name, attribute_value, attribute_description=None):
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO attribute (attribute_name, attribute_value, attribute_description)
    VALUES (%s, %s, %s)
    """
    
    cursor.execute(insert_query, (attribute_name, attribute_value, attribute_description))
    connection.commit()
    cursor.close()

def insert_category_description(connection, category_subcategory_name, category_description=None):
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO category_description (category_subcategory_name, category_description)
    VALUES (%s, %s)
    """
    
    cursor.execute(insert_query, (category_subcategory_name, category_description))
    connection.commit()
    cursor.close()

def insert_instance(connection, category_description_id, instance_count=0, first_annotation_id=None, last_annotation_id=None):
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO instance (category_description_id, instance_count, first_annotation_id, last_annotation_id)
    VALUES (%s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (category_description_id, instance_count, first_annotation_id, last_annotation_id))
    connection.commit()
    cursor.close()

def add_log_info(conn, log_name, log_date, map_id, vehicle_id):
    """插入日志信息"""
    cursor = conn.cursor()
    cursor.execute(
        """ SELECT log_info_id FROM log_info 
            WHERE log_name = %s AND log_date = %s AND map_id = %s AND vehicle_id = %s
        """,
        (log_name, log_date, map_id, vehicle_id)
    )
    result = cursor.fetchone()
    if result:
        return result[0]  # 返回已存在记录的主键
    # 如果不存在，插入新记录
    cursor.execute(
        """INSERT INTO log_info (log_name, log_date, map_id, vehicle_id)
           VALUES (%s, %s, %s, %s)""",
        (log_name, log_date, map_id, vehicle_id)
    )
    conn.commit()
    return cursor.lastrowid

def insert_map_info(conn, location, filename, version, category):
    """插入地图信息，如果已经存在则返回主键"""
    cursor = conn.cursor()
    cursor.execute(
        """ SELECT map_id FROM map_info 
            WHERE location = %s AND filename = %s AND category = %s
        """,
        (location, filename,  category)
    )
    result = cursor.fetchone()
    if result:
        return result[0]  # 返回已存在记录的主键

    # 如果不存在，插入新记录
    cursor.execute(
        "INSERT INTO map_info (location, filename, version, category) VALUES (%s, %s, %s, %s)",
        (location, filename, version, category)
    )
    conn.commit()
    return cursor.lastrowid

def insert_sensor(conn, sensor_type, sensor_name):
    """插入传感器信息"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor (sensor_type, sensor_name) VALUES (%s, %s)",
        (sensor_type, sensor_name)
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

# 插入calibrated_sensor数据
def quaternion_to_euler(rotation):
    """
    将四元数转换为欧拉角（Yaw, Pitch, Roll）。
    
    参数:
    rotation (list): 包含四元数的四个元素 [qw, qx, qy, qz]。
    
    返回:
    tuple: (yaw, pitch, roll)，单位为度。
    """
    qw, qx, qy, qz = rotation

    # 计算 Yaw (Z 轴旋转)
    yaw = math.atan2(2.0 * (qw * qz + qx * qy), 1.0 - 2.0 * (qy * qy + qz * qz))

    # 计算 Pitch (Y 轴旋转)
    pitch = math.asin(max(-1.0, min(1.0, 2.0 * (qw * qy - qz * qx))))

    # 计算 Roll (X 轴旋转)
    roll = math.atan2(2.0 * (qw * qx + qy * qz), 1.0 - 2.0 * (qx * qx + qy * qy))

    # 转换为度
    yaw_deg = math.degrees(yaw)
    pitch_deg = math.degrees(pitch)
    roll_deg = math.degrees(roll)

    return yaw_deg, pitch_deg, roll_deg

def insert_sensor_calibration(connection, sensor_id, calibration_reference=None, 
                              self_coordinates_x=None, self_coordinates_y=None, self_coordinates_z=None,
                              translation_x=None, translation_y=None, translation_z=None,
                              rotation_roll=None, rotation_pitch=None, rotation_yaw=None,
                              focal_length_x=None, focal_length_y=None,
                              principal_point_x=None, principal_point_y=None,
                              radial_distortion_k1=None, radial_distortion_k2=None, radial_distortion_k3=None,
                              tangential_distortion_p1=None, tangential_distortion_p2=None):
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO sensor_calibration (
        sensor_id, calibration_reference,
        self_coordinates_x, self_coordinates_y, self_coordinates_z,
        translation_x, translation_y, translation_z,
        rotation_roll, rotation_pitch, rotation_yaw,
        focal_length_x, focal_length_y,
        principal_point_x, principal_point_y,
        radial_distortion_k1, radial_distortion_k2, radial_distortion_k3,
        tangential_distortion_p1, tangential_distortion_p2
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
        
    cursor.execute(insert_query, (
        sensor_id, calibration_reference,
        self_coordinates_x, self_coordinates_y, self_coordinates_z,
        translation_x, translation_y, translation_z,
        rotation_roll, rotation_pitch, rotation_yaw,
        focal_length_x, focal_length_y,
        principal_point_x, principal_point_y,
        radial_distortion_k1, radial_distortion_k2, radial_distortion_k3,
        tangential_distortion_p1, tangential_distortion_p2
    ))


    connection.commit()
    cursor.close()

def add_sensor_data(conn, timestamp, sensor_calibration_id, data_file_format, file_path,
                      previous_sensor_data_id=None, next_sensor_data_id=None, image_width=None,
                      image_height=None, is_key_frame=0, ego_translation_x=None,
                      ego_translation_y=None, ego_translation_z=None, ego_rotation_roll=None,
                      ego_rotation_pitch=None, ego_rotation_yaw=None, sample_id=None):
    """插入传感器数据"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sensor_data (
            timestamp, sensor_calibration_id, data_file_format, file_path,
            previous_sensor_data_id, next_sensor_data_id, image_width,
            image_height, is_key_frame, ego_translation_x, ego_translation_y,
            ego_translation_z, ego_rotation_roll, ego_rotation_pitch,
            ego_rotation_yaw, sample_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (timestamp, sensor_calibration_id, data_file_format, file_path,
         previous_sensor_data_id, next_sensor_data_id, image_width,
         image_height, is_key_frame, ego_translation_x, ego_translation_y,
         ego_translation_z, ego_rotation_roll, ego_rotation_pitch,
         ego_rotation_yaw, sample_id)
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

def update_next_sample_id(conn, current_id, prev_id):
    """更新前一个样本的 next_sample_id"""
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sample_info SET next_sample_id = %s WHERE sample_id = %s",
            (current_id, prev_id)
        )
        conn.commit()

def add_sample_annotation(conn, sample_id, bbox_center_3d_x=None, bbox_center_3d_y=None, bbox_center_3d_z=None,
                             bbox_3d_width_y=None, bbox_3d_height_z=None, bbox_3d_length_x=None,
                             bbox_2d_xmin=None, bbox_2d_ymin=None, bbox_2d_xmax=None, bbox_2d_ymax=None,
                             bbox_2d_pixel_count=None, previous_annotation_id=None, next_annotation_id=None,
                             num_lidar_pts=0, num_radar_pts=0, rotation_roll=None, rotation_pitch=None,
                             rotation_yaw=None, instance_id=None):
    """插入样本注释"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sample_annotation (
            sample_id, bbox_center_3d_x, bbox_center_3d_y, bbox_center_3d_z,
            bbox_3d_width_y, bbox_3d_height_z, bbox_3d_length_x, bbox_2d_xmin,
            bbox_2d_xmax, bbox_2d_ymin, bbox_2d_ymax, bbox_2d_pixel_count,
            previous_annotation_id, next_annotation_id, num_lidar_pts,
            num_radar_pts, rotation_roll, rotation_pitch, rotation_yaw, instance_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (sample_id, bbox_center_3d_x, bbox_center_3d_y, bbox_center_3d_z,
         bbox_3d_width_y, bbox_3d_height_z, bbox_3d_length_x, bbox_2d_xmin,
         bbox_2d_xmax, bbox_2d_ymin, bbox_2d_ymax, bbox_2d_pixel_count,
         previous_annotation_id, next_annotation_id, num_lidar_pts,
         num_radar_pts, rotation_roll, rotation_pitch, rotation_yaw, instance_id)
    )
    conn.commit()
    return cursor.lastrowid

def insert_semantic_segmentation(
    connection, sensor_data_id, segmentation_type, segment_boundary=None,
    pixel_count=None, point_count=None, confidence=None, category_description_id=None
):
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO semantic_segmentation (
        sensor_data_id, segmentation_type, segment_boundary, pixel_count,
        point_count, confidence, category_description_id
    ) VALUES (%s, %s, ST_GeomFromText(%s), %s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (
        sensor_data_id, segmentation_type, segment_boundary,
        pixel_count, point_count, confidence, category_description_id
    ))
    connection.commit()
    cursor.close()

def process_nuscenes_training_data(conn):
    """处理 nuscene 数据集并插入数据库"""
    for scene_item in nusc.scene:
        first_sample_id = None
        previous_sample_id = None
        log_item = nusc.get("log",scene_item["log_token"])
        map_item = nusc.get("map",log_item["map_token"])
        map_id = insert_map_info(conn, log_item["location"], map_item["filename"], None, map_item["category"])
        log_info_id = add_log_info(conn, log_item["logfile"], log_item["date_captured"], map_id, log_item["vehicle"])
        scene_id = add_scene_info(conn, scene_item["description"], log_info_id)

        # 插入样本信息
        # 创建一个数组来存储每个场景的样本
        scene_samples = []
        scene_token = scene_item["token"]
        # 找到该场景的所有样本
        for sample_item in nusc.sample:
            if sample_item["scene_token"] == scene_token:
                scene_samples.append(sample_item)

        for index in scene_samples :
            second_timestamp = index["timestamp"] / 1_000_000
            dt_object = datetime.datetime.fromtimestamp(second_timestamp)
            formatted_timestamp = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')
            sample_id = add_sample_info(conn, formatted_timestamp, scene_id, previous_sample_id, None)
            if previous_sample_id:
                update_next_sample_id(conn, sample_id, previous_sample_id)
            previous_sample_id = sample_id
            if not first_sample_id:
                first_sample_id = sample_id

        
        

    print("数据集数据插入完成")


if __name__ == "__main__":
    """主函数：连接数据库、处理并插入 nuscene 数据集"""
    conn = connect_database()
    process_nuscenes_training_data(conn)