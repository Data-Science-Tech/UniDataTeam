import time
import datetime
import mysql.connector

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'car_perception_db'
}

# Debug 模式开关
DEBUG_MODE = True  # 设置为 True 开启调试信息，设置为 False 禁用调试信息

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
    # 1. 检查映射表中是否存在 token 映射
    query = f"""
    SELECT id FROM {source_table}
    WHERE token = %s AND source_table = %s
    """
    cursor.execute(query, (token, target_table))
    result = cursor.fetchone()

    if result:
        # 如果映射已存在，返回对应的 ID
        debug_print(f"Found existing mapping: token={token}, source_table={target_table}, id={result[0]}")
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


def main():
    # 连接到数据库
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # 加载 nuScenes 数据集
    from nuscenes.nuscenes import NuScenes
    nusc = NuScenes(version='v1.0-mini', dataroot=r'D:\datasets\nuScenes\v1.0-mini', verbose=True)

    try:
        # 禁用外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        debug_print("Foreign key checks disabled.")

        # 开始事务
        connection.start_transaction()

        # --------------------------------------------------
        # 遍历所有 scene 并插入到数据库
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
        for sensor in nusc.sensor:
            sensor_id = get_or_create_mapping(cursor, sensor['token'], 'nuscene_token_to_id', 'sensor', 'sensor_id')
            insert_sensor(cursor, sensor_id, sensor['modality'], sensor['channel'])

        # --------------------------------------------------
        # 遍历所有 calibrated_sensor 并插入到数据库
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
            
        

        # 提交事务
        connection.commit()
        debug_print("Transaction committed successfully.")

    except Exception as e:
        # 如果发生错误，回滚事务
        connection.rollback()
        debug_print(f"Transaction rolled back due to error: {e}")

    finally:
        # 恢复外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        debug_print("Foreign key checks enabled.")

        # 关闭数据库连接
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
