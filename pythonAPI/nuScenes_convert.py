from doctest import debug
import time
import datetime
from flask.debughelpers import DebugFilesKeyError
import mysql.connector
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import Box
from nuscenes.utils.geometry_utils import view_points
import numpy as np

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'car_perception_db'
}

# Debug 模式开关
DEBUG_MODE = False  # 设置为 True 开启调试信息，设置为 False 禁用调试信息

class Custom3DBox:
    def __init__(self, translation, size, rotation):
        """
        初始化 3D 边界框
        :param translation: 3D 中心坐标 [x, y, z]
        :param size: 3D 尺寸 [width, length, height]
        :param rotation: 3D 四元数 [w, x, y, z]
        """
        self.translation = np.array(translation)  # 中心位置
        self.size = np.array(size)                # 尺寸
        self.rotation = np.array(rotation)        # 四元数旋转

        # 检查四元数是否归一化
        norm = np.linalg.norm(self.rotation)
        if not np.isclose(norm, 1.0, atol=1e-6):
            self.rotation = self.rotation / norm
            print("Rotation quaternion was not normalized. Normalized it.")

    def corners(self):
        """
        计算 3D 边界框的 8 个角点坐标（局部坐标系）
        :return: 8 个角点的 3D 坐标
        """
        width, length, height = self.size / 2.0  # 半尺寸
        # 定义局部坐标系中的角点位置
        corners = np.array([
            [width, length, height],
            [width, length, -height],
            [width, -length, height],
            [width, -length, -height],
            [-width, length, height],
            [-width, length, -height],
            [-width, -length, height],
            [-width, -length, -height]
        ])
        return corners

    def transform(self):
        """
        将局部坐标系中的角点变换到全局坐标系
        :return: 变换后的 8 个角点的 3D 坐标
        """
        # 获取角点
        corners = self.corners()
        # 计算旋转矩阵
        rotation_matrix = self.quaternion_to_rotation_matrix(self.rotation)
        # 应用旋转和平移
        transformed_corners = np.dot(rotation_matrix, corners.T).T + self.translation
        return transformed_corners

    @staticmethod
    def quaternion_to_rotation_matrix(quaternion):
        """
        将四元数转换为旋转矩阵
        :param quaternion: 四元数 [w, x, y, z]
        :return: 旋转矩阵 (3x3)
        """
        w, x, y, z = quaternion
        return np.array([
            [1 - 2 * (y**2 + z**2), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x**2 + z**2), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x**2 + y**2)]
        ])


def debug_print(message):
    """
    打印调试信息，仅在 DEBUG_MODE 为 True 时生效
    :param message: 要打印的调试信息
    """
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

def get_or_create_mapping(cursor, token, source_table, target_table, id_column):
    """
    获取或生成一个表（如 scene 表）中主键 ID 对应的 token 映射。
    :param cursor: MySQL 数据库游标
    :param token: nuScenes 的 token (字符串)
    :param source_table: 映射表的名称（如 nuscene_token_to_id）
    :param target_table: 目标表的名称（如 scene 表）
    :param id_column: 目标表的主键列名称（如 scene_id）
    :return: 返回映射的 ID
    """
    if not token or token == '':
        debug_print(f"NULL token: {token}\n")
        return None

    # 1. 检查映射表中是否存在 token 映射
    query = f"""
    SELECT id FROM {source_table}
    WHERE token = %s AND source_table = %s
    """
    cursor.execute(query, (token, target_table))
    result = cursor.fetchone()

    if result:
        # 如果映射已存在，返回对应的 ID
        debug_print(f"Found existing mapping: token={token}, source_table={target_table}, id={result[0]}\n")
        return result[0]

    debug_print(f"No mapping found for token={token}, source_table={target_table}")

    # 2. 查询映射表中当前 source_table 的最大 ID
    max_mapping_id_query = f"""
    SELECT MAX(id) FROM {source_table}
    WHERE source_table = %s
    """
    cursor.execute(max_mapping_id_query, (target_table,))
    max_mapping_id_result = cursor.fetchone()
    max_mapping_id = max_mapping_id_result[0] if max_mapping_id_result and max_mapping_id_result[0] else 0

    debug_print(f"Current max ID in source_table={source_table} for source_table={target_table}: {max_mapping_id}")

    # 3. 查询目标表中的最大 ID
    max_id_query = f"SELECT MAX({id_column}) FROM {target_table}"
    cursor.execute(max_id_query)
    max_id_result = cursor.fetchone()
    max_id = max_id_result[0] if max_id_result and max_id_result[0] else 0

    debug_print(f"Current max ID in target_table={target_table}, id_column={id_column}: {max_id}")

    # 4. 生成新的 ID，取映射表和目标表中的最大 ID
    new_id = max(max_mapping_id, max_id) + 1
    debug_print(f"Generated new ID: {new_id}")

    # 5. 插入新的映射到映射表
    insert_query = f"""
    INSERT INTO {source_table} (token, source_table, id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (token, target_table, new_id))
    debug_print(f"Inserted new mapping: token={token}, source_table={target_table}, id={new_id}")
    debug_print("\n")

    return new_id

def insert_scene_info(cursor, scene_id, description, log_id, sample_count, first_sample_id, last_sample_id):
    """
    插入一条 scene 信息到 scene_info 表中
    """
    sql = """
    INSERT INTO scene_info (scene_id, scene_description, log_info_id, sample_count, first_sample_id, last_sample_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (scene_id, description, log_id, sample_count, first_sample_id, last_sample_id)
    cursor.execute(sql, data)

def get_or_insert_map_info(cursor, name, location, filename, version, category):
    """
    获取或插入 map_info 表中的记录。
    如果记录存在，则返回现有的 map_id。
    如果记录不存在，则插入新记录并返回新生成的 map_id。
    """
    # 1. 检查是否存在完全相同的记录
    select_query = """
    SELECT map_id FROM map_info
    WHERE name = %s AND location = %s AND filename = %s AND version = %s AND category = %s
    """
    cursor.execute(select_query, (name, location, filename, version, category))
    result = cursor.fetchone()

    if result:
        # 如果记录存在，返回现有的 map_id
        debug_print(f"Found existing map_info record with map_id={result[0]}")
        return result[0]

    # 2. 如果记录不存在，插入新记录
    debug_print("No matching map_info record found. Inserting new record.")
    insert_query = """
    INSERT INTO map_info (name, location, filename, version, category)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, location, filename, version, category))

    # 3. 获取新插入记录的 map_id
    cursor.execute("SELECT LAST_INSERT_ID()")
    new_map_id = cursor.fetchone()[0]
    debug_print(f"Inserted new map_info record with map_id={new_map_id}")

    return new_map_id


def insert_log_info(cursor, log_id, log_name, log_date, map_id, vehicle_id):
    """
    插入 log 信息到 log_info 表中
    """
    sql = """
    INSERT INTO log_info (log_info_id, log_name, log_date, map_id, vehicle_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (log_id, log_name, log_date, map_id, vehicle_id)
    cursor.execute(sql, data)

def insert_sample_info(cursor, sample_id, timestamp, scene_id, previous_sample_id, next_sample_id):
    """
    插入一条 sample 信息到 sample_info 表中
    :param cursor: 数据库游标
    :param sample_id: 样本的唯一 ID
    :param timestamp: 时间戳
    :param scene_id: 场景 ID
    :param previous_sample_id: 前一个样本 ID
    :param next_sample_id: 下一个样本 ID
    """
    sql = """
    INSERT INTO sample_info (sample_id, timestamp, scene_id, previous_sample_id, next_sample_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (sample_id, timestamp, scene_id, previous_sample_id, next_sample_id)
    cursor.execute(sql, data)

def insert_sensor(cursor, sensor_id, sensor_type, sensor_name):
    """
    插入一条 sensor 信息到 sensor 表中
    """
    sql = """
    INSERT INTO sensor (sensor_id, sensor_type, sensor_name)
    VALUES (%s, %s, %s)
    """
    data = (sensor_id, sensor_type, sensor_name)
    cursor.execute(sql, data)

def insert_sensor_calibration(cursor, sensor_calibration_id, sensor_id, calibration_reference, 
                              self_coordinates_x, self_coordinates_y, self_coordinates_z,
                              translation_x, translation_y, translation_z, 
                              rotation_qw, rotation_qx, rotation_qy, rotation_qz, 
                              focal_length_x, focal_length_y, 
                              principal_point_x, principal_point_y, 
                              radial_distortion_k1, radial_distortion_k2, radial_distortion_k3, 
                              tangential_distortion_p1, tangential_distortion_p2):
    """
    插入一条 sensor_calibration 信息到 sensor_calibration 表中。
    :param cursor: 数据库游标
    :param sensor_calibration_id: 主键 ID（可通过外部生成或自增管理）
    :param sensor_id: 对应 sensor 表的 ID
    :param calibration_reference: 标定参考
    :param self_coordinates_x/y/z: 自身坐标
    :param translation_x/y/z: 传感器外参位移
    :param rotation_qw/qx/qy/qz: 传感器外参旋转四元数
    :param focal_length_x/y: 摄像机内参焦距
    :param principal_point_x/y: 摄像机内参主点
    :param radial_distortion_k1/k2/k3: 径向畸变参数
    :param tangential_distortion_p1/p2: 切向畸变参数
    """
    sql = """
    INSERT INTO sensor_calibration (
        sensor_calibration_id, sensor_id, calibration_reference, 
        self_coordinates_x, self_coordinates_y, self_coordinates_z, 
        translation_x, translation_y, translation_z, 
        rotation_qw, rotation_qx, rotation_qy, rotation_qz, 
        focal_length_x, focal_length_y, 
        principal_point_x, principal_point_y, 
        radial_distortion_k1, radial_distortion_k2, radial_distortion_k3, 
        tangential_distortion_p1, tangential_distortion_p2
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        sensor_calibration_id, sensor_id, calibration_reference,
        self_coordinates_x, self_coordinates_y, self_coordinates_z,
        translation_x, translation_y, translation_z,
        rotation_qw, rotation_qx, rotation_qy, rotation_qz,
        focal_length_x, focal_length_y,
        principal_point_x, principal_point_y,
        radial_distortion_k1, radial_distortion_k2, radial_distortion_k3,
        tangential_distortion_p1, tangential_distortion_p2
    )
    cursor.execute(sql, data)

def insert_sensor_data(cursor, sensor_data_id, timestamp, sensor_calibration_id, data_file_format, 
                        previous_sensor_data_id, next_sensor_data_id, image_width, image_height, 
                        file_path, is_key_frame, ego_translation_x, ego_translation_y, ego_translation_z, 
                        ego_rotation_qw, ego_rotation_qx, ego_rotation_qy, ego_rotation_qz, sample_id):
    """
    插入一条 sensor_data 信息到 sensor_data 表中
    """
    sql = """
    INSERT INTO sensor_data (
        sensor_data_id, timestamp, sensor_calibration_id, data_file_format, 
        previous_sensor_data_id, next_sensor_data_id, image_width, image_height, 
        file_path, is_key_frame, ego_translation_x, ego_translation_y, ego_translation_z, 
        ego_rotation_qw, ego_rotation_qx, ego_rotation_qy, ego_rotation_qz, sample_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        sensor_data_id, timestamp, sensor_calibration_id, data_file_format, 
        previous_sensor_data_id, next_sensor_data_id, image_width, image_height, 
        file_path, is_key_frame, ego_translation_x, ego_translation_y, ego_translation_z, 
        ego_rotation_qw, ego_rotation_qx, ego_rotation_qy, ego_rotation_qz, sample_id
    )
    cursor.execute(sql, data)

def insert_sample_annotation(cursor, annotation_id, sample_id, bbox_center_3d_x, bbox_center_3d_y, bbox_center_3d_z,
                             bbox_3d_width_y, bbox_3d_height_z, bbox_3d_length_x, previous_annotation_id, next_annotation_id,
                             num_lidar_pts, num_radar_pts, rotation_qw, rotation_qx, rotation_qy, rotation_qz, instance_id):
    """
    插入一条 sample_annotation 信息到 sample_annotation 表中
    """
    sql = """
    INSERT INTO sample_annotation (
        annotation_id, sample_id, bbox_center_3d_x, bbox_center_3d_y, bbox_center_3d_z,
        bbox_3d_width_y, bbox_3d_height_z, bbox_3d_length_x, previous_annotation_id, next_annotation_id,
        num_lidar_pts, num_radar_pts, rotation_qw, rotation_qx, rotation_qy, rotation_qz, instance_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        annotation_id, sample_id, bbox_center_3d_x, bbox_center_3d_y, bbox_center_3d_z,
        bbox_3d_width_y, bbox_3d_height_z, bbox_3d_length_x, previous_annotation_id, next_annotation_id,
        num_lidar_pts, num_radar_pts, rotation_qw, rotation_qx, rotation_qy, rotation_qz, instance_id
    )
    cursor.execute(sql, data)

def insert_annotation_2d(cursor, bbox_2d_xmin, bbox_2d_xmax, bbox_2d_ymin, bbox_2d_ymax, sample_annotation_id, sensor_data_id):
    """
    插入一条 annotation_2d 信息到 annotaion_2d 表中
    """
    sql = """
    INSERT INTO annotaion_2d (bbox_2d_xmin, bbox_2d_xmax, bbox_2d_ymin, bbox_2d_ymax, sample_annotation_id, sensor_data_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (bbox_2d_xmin, bbox_2d_xmax, bbox_2d_ymin, bbox_2d_ymax, sample_annotation_id, sensor_data_id)
    cursor.execute(sql, data)

def insert_attribute(cursor, attribute_id, attribute_name, attribute_value, attribute_description=None):
    """
    插入一条 attribute 信息到 attribute 表中
    """
    sql = """
    INSERT INTO attribute (attribute_id, attribute_name, attribute_value, attribute_description)
    VALUES (%s, %s, %s, %s)
    """
    data = (attribute_id, attribute_name, attribute_value, attribute_description)
    cursor.execute(sql, data)

def insert_annotation_attribute(cursor, annotation_id, attribute_id):
    """
    插入一条 annotation_attribute 信息到 annotation_attribute 表中
    """
    sql = """
    INSERT INTO annotation_attribute (annotation_id, attribute_id)
    VALUES (%s, %s)
    """
    data = (annotation_id, attribute_id)
    cursor.execute(sql, data)

def insert_instance(cursor, instance_id, category_description_id, instance_count, first_annotation_id, last_annotation_id):
    """
    插入一条 instance 信息到 instance 表中
    """
    sql = """
    INSERT INTO instance (instance_id, category_description_id, instance_count, first_annotation_id, last_annotation_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (instance_id, category_description_id, instance_count, first_annotation_id, last_annotation_id)
    cursor.execute(sql, data)

def insert_category_description(cursor, category_description_id, category_name, category_description):
    """
    插入一条 category_description 信息到 category_description 表中
    """
    sql = """
    INSERT INTO category_description (category_description_id, category_subcategory_name, category_description)
    VALUES (%s, %s, %s)
    """
    data = (category_description_id, category_name, category_description)
    cursor.execute(sql, data)

import numpy as np

def get_2d_bbox_from_annotation_auto_obj(cursor, nusc, sample_annotation, debug=False):
    """
    根据 sample_annotation 对象，通过 sample -> sample_data -> calibrated_sensor -> sensor 的逐级查找，
    生成所有相机视角的 2D 边界框，并插入到数据库，同时移除外部依赖包，手动计算所有变换。

    :param cursor: 数据库游标对象，用于插入数据。
    :param nusc: NuScenes 数据集对象。
    :param sample_annotation: sample_annotation 的字典对象。
    :param debug: 是否打印调试信息 (默认 False)。
    """
    def debug_print(message):
        """根据 debug 标志控制打印输出"""
        if debug:
            print(message)

    def quaternion_to_rotation_matrix(quaternion):
        """
        将四元数转换为旋转矩阵
        :param quaternion: 四元数 [w, x, y, z]
        :return: 旋转矩阵 (3x3)
        """
        w, x, y, z = quaternion
        norm = np.sqrt(w**2 + x**2 + y**2 + z**2)
        w, x, y, z = w / norm, x / norm, y / norm, z / norm  # 归一化
        return np.array([
            [1 - 2 * (y**2 + z**2), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x**2 + z**2), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x**2 + y**2)]
        ])


    def compute_box_corners(translation, size, rotation):
        """
        计算 3D 边界框的 8 个角点坐标
        :param translation: 中心点坐标 [x, y, z]
        :param size: 尺寸 [width, length, height]
        :param rotation: 四元数 [w, x, y, z]
        :return: 全局坐标系下的 8 个角点 (8x3 数组)
        """
        width, length, height = size[0] / 2.0, size[1] / 2.0, size[2] / 2.0  # 半尺寸
        # 局部坐标系中的 8 个角点
        corners = np.array([
            [width, length, height],
            [width, length, -height],
            [width, -length, height],
            [width, -length, -height],
            [-width, length, height],
            [-width, length, -height],
            [-width, -length, height],
            [-width, -length, -height]
        ])
        # 应用旋转和平移
        rotation_matrix = quaternion_to_rotation_matrix(rotation)
        corners = np.dot(rotation_matrix, corners.T).T + np.array(translation)
        return corners

    def project_to_2d(corners, intrinsic):
        """
        将 3D 角点投影到 2D 图像平面
        :param corners: 3D 角点 (8x3)
        :param intrinsic: 相机内参矩阵 (3x3)
        :return: 投影到图像上的 2D 坐标 (2x8)
        """
        # 转换为齐次坐标
        corners_homogeneous = np.hstack((corners, np.ones((corners.shape[0], 1))))  # (8, 4)
        corners_homogeneous = corners_homogeneous.T  # 转置为 (4, 8)

        # 投影到 2D
        projected = np.dot(intrinsic, corners_homogeneous[:3, :])  # (3, 8)
        projected[2, :] = np.maximum(projected[2, :], 1e-6)  # 防止 z 值为零
        projected /= projected[2, :]  # 归一化

        return projected[:2, :]  # 返回 2D 坐标

    # 1. 从 sample_annotation 获取 sample
    sample_token = sample_annotation['sample_token']
    sample = nusc.get('sample', sample_token)
    debug_print(f"[Step 1] Sample loaded. Sample token: {sample_token}")

    # 2. 遍历 sample 的所有 sample_data
    for sample_data_token in sample['data'].values():
        # 3. 获取 sample_data 对象
        sample_data = nusc.get('sample_data', sample_data_token)
        debug_print(f"[Step 2] Sample data loaded. Token: {sample_data_token}, File format: {sample_data['fileformat']}, Height: {sample_data.get('height', 'N/A')}")

        # 4. 获取 calibrated_sensor 信息
        calibrated_sensor = nusc.get('calibrated_sensor', sample_data['calibrated_sensor_token'])
        debug_print(f"[Step 3] Calibrated sensor loaded. Token: {sample_data['calibrated_sensor_token']}")

        # 5. 获取 sensor 信息
        sensor = nusc.get('sensor', calibrated_sensor['sensor_token'])
        debug_print(f"[Step 4] Sensor loaded. Sensor name: {sensor['channel']}")

        # 6. 检查是否为相机传感器
        if 'CAM' not in sensor['channel']:
            debug_print(f"[Step 5] Skipped. Not a camera sensor. Channel: {sensor['channel']}")
            continue

        # 7. 获取相机内参和图像分辨率
        intrinsic = np.array(calibrated_sensor['camera_intrinsic'])
        imsize = (sample_data['width'], sample_data['height'])  # 图像分辨率
        debug_print(f"[Step 6] Camera intrinsic matrix: {intrinsic}, Image size: {imsize}")

        # 8. 计算 3D 边界框角点
        corners = compute_box_corners(
            translation=sample_annotation['translation'],
            size=sample_annotation['size'],
            rotation=sample_annotation['rotation']
        )
        debug_print(f"[Step 7] Corners in global coordinates: {corners}")

        # 9. 投影到图像平面
        projected_corners = project_to_2d(corners, intrinsic)
        debug_print(f"[Step 8] Projected corners: {projected_corners}")

        # 检查是否在图像范围内
        if np.all((projected_corners[0] >= 0) & (projected_corners[0] <= imsize[0]) &
                  (projected_corners[1] >= 0) & (projected_corners[1] <= imsize[1])):

            # 计算 2D 边界框
            xmin = int(max(0, np.min(projected_corners[0])))
            xmax = int(min(imsize[0], np.max(projected_corners[0])))
            ymin = int(max(0, np.min(projected_corners[1])))
            ymax = int(min(imsize[1], np.max(projected_corners[1])))
            bbox_2d_pixel_count = (xmax - xmin) * (ymax - ymin)
            debug_print(f"[Step 9] 2D Bounding box: xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}, pixel count={bbox_2d_pixel_count}")

            # 构造 2D 边界框字典
            bbox_2d = {
                'bbox_2d_xmin': xmin,
                'bbox_2d_xmax': xmax,
                'bbox_2d_ymin': ymin,
                'bbox_2d_ymax': ymax,
                'bbox_2d_pixel_count': bbox_2d_pixel_count
            }

            # 10. 获取或创建数据库中的 sample_annotation_id 和 sensor_data_id
            sample_annotation_id = get_or_create_mapping(cursor, sample_annotation['token'], 'nuscene_token_to_id', 'sample_annotation', 'annotation_id')
            sensor_data_id = get_or_create_mapping(cursor, sample_data['token'], 'nuscene_token_to_id', 'sensor_data', 'sensor_data_id')
            debug_print(f"[Step 10] Database IDs: sample_annotation_id={sample_annotation_id}, sensor_data_id={sensor_data_id}")

            # 11. 插入 2D 边界框到数据库
            insert_annotation_2d(cursor, bbox_2d['bbox_2d_xmin'], bbox_2d['bbox_2d_xmax'],
                                    bbox_2d['bbox_2d_ymin'], bbox_2d['bbox_2d_ymax'],
                                    sample_annotation_id, sensor_data_id)
            debug_print(f"[Step 11] Bounding box inserted into database.")


def main():
    # 连接到数据库
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # 加载 nuScenes 数据集
    nusc = NuScenes(version='v1.0-mini', dataroot=r'D:\datasets\nuScenes\v1.0-mini', verbose=True)

    try:
        # 禁用外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        print("Foreign key checks disabled.")

        # 开始事务
        connection.start_transaction()

        # --------------------------------------------------
        # 遍历所有 scene 并插入到数据库
        print("Inserting scene data...")
        for scene in nusc.scene:
            # 获取或生成映射
            scene_id = get_or_create_mapping(cursor, scene['token'], 'nuscene_token_to_id', 'scene_info', 'scene_id')
            log_id = get_or_create_mapping(cursor, scene['log_token'], 'nuscene_token_to_id', 'log_info', 'log_info_id')
            first_sample_id = get_or_create_mapping(cursor, scene['first_sample_token'], 'nuscene_token_to_id', 'sample_info', 'sample_id')
            last_sample_id = get_or_create_mapping(cursor, scene['last_sample_token'], 'nuscene_token_to_id', 'sample_info', 'sample_id')

            # 提取其他字段
            description = scene['description']
            sample_count = scene['nbr_samples']

            # 插入 scene_info 数据
            insert_scene_info(cursor, scene_id, description, log_id, sample_count, first_sample_id, last_sample_id)

        # --------------------------------------------------
        # 遍历所有 log 并插入到数据库
        print("Inserting log data...")
        for log in nusc.log:
            # 获取或生成映射
            log_id = get_or_create_mapping(cursor, log['token'], 'nuscene_token_to_id', 'log_info', 'log_info_id')

            for map in nusc.map:
                if log['token'] in map['log_tokens']:
                    map_id = get_or_insert_map_info(cursor, '', log['location'], map['filename'], '', map['category'])
                    break
            
            insert_log_info(cursor, log_id, log['logfile'], log['date_captured'], map_id, log['vehicle'])

        # --------------------------------------------------
        # 遍历所有 sample 并插入到数据库
        print("Inserting sample data...")
        for sample in nusc.sample:
            sample_id = get_or_create_mapping(cursor, sample['token'], 'nuscene_token_to_id', 'sample_info', 'sample_id')
            scene_id = get_or_create_mapping(cursor, sample['scene_token'], 'nuscene_token_to_id', 'scene_info', 'scene_id')
            next_sample_id = get_or_create_mapping(cursor, sample['next'], 'nuscene_token_to_id', 'sample_info', 'sample_id')
            prev_sample_id = get_or_create_mapping(cursor, sample['prev'], 'nuscene_token_to_id', 'sample_info', 'sample_id')

            timestamp = datetime.datetime.utcfromtimestamp(sample['timestamp'] / 1000000.0)

            # 插入 sample_info 数据
            insert_sample_info(cursor, sample_id, timestamp, scene_id, prev_sample_id, next_sample_id)

        # --------------------------------------------------
        # 遍历所有 sensor 并插入到数据库
        print("Inserting sensor data...")
        for sensor in nusc.sensor:
            sensor_id = get_or_create_mapping(cursor, sensor['token'], 'nuscene_token_to_id', 'sensor', 'sensor_id')
            insert_sensor(cursor, sensor_id, sensor['modality'], sensor['channel'])

        # --------------------------------------------------
        # 遍历所有 calibrated_sensor 并插入到数据库
        print("Inserting sensor calibration data...")
        for calibrated_sensor in nusc.calibrated_sensor:
            sensor_id = get_or_create_mapping(cursor, calibrated_sensor['sensor_token'], 'nuscene_token_to_id', 'sensor', 'sensor_id')
            calibrated_sensor_id = get_or_create_mapping(cursor, calibrated_sensor['token'], 'nuscene_token_to_id', 'sensor_calibration', 'sensor_calibration_id')

            translation_x, translation_y, translation_z = calibrated_sensor["translation"]
            rotation_qw, rotation_qx, rotation_qy, rotation_qz = calibrated_sensor["rotation"]

            # 提取内参信息
            camera_intrinsic = calibrated_sensor.get("camera_intrinsic", None)
            if camera_intrinsic:
                focal_length_x = camera_intrinsic[0][0]
                focal_length_y = camera_intrinsic[1][1]
                principal_point_x = camera_intrinsic[0][2]
                principal_point_y = camera_intrinsic[1][2]
            else:
                # 如果内参不存在（如 LIDAR），使用默认值或 NULL
                focal_length_x = None
                focal_length_y = None
                principal_point_x = None
                principal_point_y = None

            # 径向和切向畸变参数（如未提供，可设为 NULL 或默认值）
            radial_distortion_k1 = None
            radial_distortion_k2 = None
            radial_distortion_k3 = None
            tangential_distortion_p1 = None
            tangential_distortion_p2 = None

            # 自身坐标 (self_coordinates) 暂时设置为 NULL
            self_coordinates_x = None
            self_coordinates_y = None
            self_coordinates_z = None

            insert_sensor_calibration(
                cursor, calibrated_sensor_id, sensor_id, None,
                self_coordinates_x, self_coordinates_y, self_coordinates_z,
                translation_x, translation_y, translation_z,
                rotation_qw, rotation_qx, rotation_qy, rotation_qz,
                focal_length_x, focal_length_y,
                principal_point_x, principal_point_y,
                radial_distortion_k1, radial_distortion_k2, radial_distortion_k3,
                tangential_distortion_p1, tangential_distortion_p2)
            
        # --------------------------------------------------
        # 遍历所有 sensor_data 并插入到数据库
        print("Inserting sensor_data data...")
        for sample_data in nusc.sample_data:
            sensor_data_id = get_or_create_mapping(cursor, sample_data['token'], 'nuscene_token_to_id', 'sensor_data', 'sensor_data_id')
            sensor_calibration_id = get_or_create_mapping(cursor, sample_data['calibrated_sensor_token'], 'nuscene_token_to_id', 'sensor_calibration', 'sensor_calibration_id')
            sample_id = get_or_create_mapping(cursor, sample_data['sample_token'], 'nuscene_token_to_id', 'sample_info', 'sample_id')
            prev_sensor_data_id = get_or_create_mapping(cursor, sample_data['prev'], 'nuscene_token_to_id', 'sensor_data', 'sensor_data_id')
            next_sensor_data_id = get_or_create_mapping(cursor, sample_data['next'], 'nuscene_token_to_id', 'sensor_data', 'sensor_data_id')

            timestamp = datetime.datetime.utcfromtimestamp(sample_data['timestamp'] / 1000000.0)
            data_file_format = sample_data['fileformat']
            image_width = sample_data['width']
            image_height = sample_data['height']
            file_path = sample_data['filename']
            is_key_frame = sample_data['is_key_frame']

            # 获取 ego pose 数据
            ego_pose = nusc.get('ego_pose', sample_data['ego_pose_token'])
            ego_translation_x, ego_translation_y, ego_translation_z = ego_pose['translation']
            ego_rotation_qw, ego_rotation_qx, ego_rotation_qy, ego_rotation_qz = ego_pose['rotation']

            insert_sensor_data(
                cursor, sensor_data_id, timestamp, sensor_calibration_id, data_file_format,
                prev_sensor_data_id, next_sensor_data_id, image_width, image_height,
                file_path, is_key_frame, ego_translation_x, ego_translation_y, ego_translation_z,
                ego_rotation_qw, ego_rotation_qx, ego_rotation_qy, ego_rotation_qz, sample_id)
            
        # --------------------------------------------------
        # 遍历所有 attribute 和 visibility 并插入到 attribute 表中
        print("Inserting attribute data...")
        for attribute in nusc.attribute:
            attribute_id = get_or_create_mapping(cursor, attribute['token'], 'nuscene_token_to_id', 'attribute', 'attribute_id')
            insert_attribute(cursor, attribute_id, attribute['name'], '', attribute['description'])
        
        for visibility in nusc.visibility:
            visibility_id = get_or_create_mapping(cursor, visibility['token'], 'nuscene_token_to_id', 'attribute', 'attribute_id')
            insert_attribute(cursor, visibility_id, 'visibility', visibility['level'], visibility['description'])

        # --------------------------------------------------
        # 遍历所有 category_description 并插入到 category_description 表中
        print("Inserting category_description data...")
        for category in nusc.category:
            category_description_id = get_or_create_mapping(cursor, category['token'], 'nuscene_token_to_id', 'category_description', 'category_description_id')
            insert_category_description(cursor, category_description_id, category['name'], category['description'])

        # --------------------------------------------------
        # 遍历所有 instance 并插入到 instance 表中
        print("Inserting instance data...")
        for instance in nusc.instance:
            instance_id = get_or_create_mapping(cursor, instance['token'], 'nuscene_token_to_id', 'instance', 'instance_id')
            category_description_id = get_or_create_mapping(cursor, instance['category_token'], 'nuscene_token_to_id', 'category_description', 'category_description_id')
            first_annotation_id = get_or_create_mapping(cursor, instance['first_annotation_token'], 'nuscene_token_to_id', 'sample_annotation', 'annotation_id')
            last_annotation_id = get_or_create_mapping(cursor, instance['last_annotation_token'], 'nuscene_token_to_id', 'sample_annotation', 'annotation_id')
            insert_instance(cursor, instance_id, category_description_id, instance['nbr_annotations'], first_annotation_id, last_annotation_id)

        # --------------------------------------------------
        # 遍历所有 sample_annotation 并插入到 sample_annotation 表中
        print("Inserting sample_annotation data...")
        for sample_annotation in nusc.sample_annotation:
            annotation_id = get_or_create_mapping(cursor, sample_annotation['token'], 'nuscene_token_to_id', 'sample_annotation', 'annotation_id')
            sample_id = get_or_create_mapping(cursor, sample_annotation['sample_token'], 'nuscene_token_to_id', 'sample_info', 'sample_id')
            previous_annotation_id = get_or_create_mapping(cursor, sample_annotation['prev'], 'nuscene_token_to_id', 'sample_annotation', 'annotation_id')
            next_annotation_id = get_or_create_mapping(cursor, sample_annotation['next'], 'nuscene_token_to_id', 'sample_annotation', 'annotation_id')
            instance_id = get_or_create_mapping(cursor, sample_annotation['instance_token'], 'nuscene_token_to_id', 'instance', 'instance_id')

            bbox_center_3d = sample_annotation['translation']
            bbox_3d_width = sample_annotation['size'][1]
            bbox_3d_height = sample_annotation['size'][2]
            bbox_3d_length = sample_annotation['size'][0]

            debug_print(f"transforming 2d bbox from annotation")
            get_2d_bbox_from_annotation_auto_obj(cursor, nusc, sample_annotation)
            
            num_lidar_pts = sample_annotation['num_lidar_pts']
            num_radar_pts = sample_annotation['num_radar_pts']
            rotation = sample_annotation['rotation']

            debug_print(f"Inserting sample_annotation into database")
            insert_sample_annotation(
                cursor, annotation_id, sample_id, bbox_center_3d[0], bbox_center_3d[1], bbox_center_3d[2],
                bbox_3d_width, bbox_3d_height, bbox_3d_length, previous_annotation_id, next_annotation_id,
                num_lidar_pts, num_radar_pts, rotation[0], rotation[1], rotation[2], rotation[3], instance_id
            )

            # 插入属性信息
            for attribute_token in sample_annotation['attribute_tokens']:
                attribute_id = get_or_create_mapping(cursor, attribute_token, 'nuscene_token_to_id', 'attribute', 'attribute_id')
                insert_annotation_attribute(cursor, annotation_id, attribute_id)

            for visibility_token in sample_annotation['visibility_token']:
                visibility_id = get_or_create_mapping(cursor, visibility_token, 'nuscene_token_to_id', 'attribute', 'attribute_id')
                insert_annotation_attribute(cursor, annotation_id, visibility_id)

        # 提交事务
        connection.commit()
        print("Transaction committed successfully.")

    except Exception as e:
        # 如果发生错误，回滚事务
        connection.rollback()
        print(f"Transaction rolled back due to error: {e}")

    finally:
        # 恢复外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("Foreign key checks enabled.")

        # 关闭数据库连接
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
