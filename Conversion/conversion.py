from nuscenes.nuscenes import NuScenes
import os
current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import mysql.connector
from mysql.connector import Error
import math
import datetime
connection = None
nusc = NuScenes(version='v1.0-mini', dataroot = current_folder + '\\v1.0-mini', verbose = True)

def connectdatabase():
    try:
        # 连接到数据库
        connection = mysql.connector.connect(
            host='localhost',      
            port=3306,              
            user='root',            
            password='qin3398466884',  
            database='car_perception_db'  
        )

        if connection.is_connected():
            print("成功连接到数据库")

        # insert_sensor(connection)
        # insert_sensor_calibration(connection)
        # insert_attribute(connection)
        # insert_map_log(connection)
        # insert_category(connection)
        # insert_scene_sample(connection)

    
    except Error as e:
        print("数据库连接或操作失败：", e)

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("数据库连接已关闭")

# 插入sensor数据
def insert_sensor(connection):
    if connection is None:
        print("无法插入数据，因为数据库连接未成功建立。")
        return    
    cursor = connection.cursor()

    # 插入数据到sensors表
    for item in nusc.sensor:
        # token = item["token"]
        channel = item["channel"]
        modality = item["modality"]
        # print(f"Token: {token}, Channel: {channel}, Modality: {modality}")

        try:
            # 执行插入SQL语句
            insert_query = """
            INSERT INTO sensor (sensor_type, sensor_name)
            VALUES (%s, %s)
            """
            cursor.execute(insert_query, (channel, modality))
        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")

    # 提交事务
    connection.commit()
    print("sensor成功插入！")
    cursor.close()

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

def insert_sensor_calibration(connection):
    cursor = connection.cursor()
    
    try:
        # 遍历 calibrated_sensor 列表
        for item in nusc.calibrated_sensor:
            try:
                # 定义查询SQL语句
                select_query = """
                SELECT sensor_id FROM sensor
                WHERE sensor_type = %s AND sensor_name = %s
                """
                temp = nusc.get('sensor', item["sensor_token"])

                # 执行查询
                cursor.execute(select_query, (temp['channel'], temp['modality']))

                # 获取查询结果并检查是否存在
                result = cursor.fetchone()
                if result is None:
                    print("未找到匹配的 sensor_id")
                    continue  # 跳过本次循环

                sensor_id = result[0]
                rotation_yaw, rotation_pitch, rotation_roll = quaternion_to_euler(item["rotation"])

                # 判断 camera_intrinsic 是否为空，插入对应的数据
                if item["camera_intrinsic"]:
                    insert_query = """
                    INSERT INTO sensor_calibration (
                        sensor_id, translation_x, translation_y, translation_z,
                        rotation_roll, rotation_pitch, rotation_yaw,
                        focal_length_x, focal_length_y, principal_point_x, principal_point_y
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        sensor_id, item["translation"][0], item["translation"][1], item["translation"][2],
                        rotation_roll, rotation_pitch, rotation_yaw,
                        item["camera_intrinsic"][0][0], item["camera_intrinsic"][1][1],
                        item["camera_intrinsic"][0][2], item["camera_intrinsic"][1][2]
                    ))
                else:
                    insert_query = """
                    INSERT INTO sensor_calibration (
                        sensor_id, translation_x, translation_y, translation_z,
                        rotation_roll, rotation_pitch, rotation_yaw
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        sensor_id, item["translation"][0], item["translation"][1], item["translation"][2],
                        rotation_roll, rotation_pitch, rotation_yaw
                    ))

            except mysql.connector.Error as e:
                print(f"Error fetching or inserting data: {e}")

        # 提交事务
        connection.commit()
        print("sensor_calibration成功插入！")

    finally:
        # 关闭游标
        cursor.close()

# 插入map_info和log_info
# map表的name改为非空约束
def insert_map_info(connection, unique_results):
    """
    将 unique_results 中的 map 信息插入到 map_info 表。
    """
    cursor = connection.cursor()
    for item in unique_results:
        category = item["category"]
        filename = item["filename"]
        location = item["location"]

        try:
            insert_query = """
            INSERT INTO map_info (location, filename, category)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (location, filename, category))
        except mysql.connector.Error as e:
            print(f"Error inserting data into map_info: {e}")

    # 提交事务
    connection.commit()
    print("map_info 表数据成功插入！")
    cursor.close()

def get_map_id(connection, filename):
    """
    根据 map 的 filename 查询 map_id。
    """
    cursor = connection.cursor()
    map_id = None
    try:
        select_query = """
        SELECT map_id FROM map_info WHERE filename = %s
        """
        cursor.execute(select_query, (filename,))
        result = cursor.fetchone()
        if result is not None:
            map_id = int(result[0])
        else:
            print("未找到匹配的 map_id")
    except mysql.connector.Error as e:
        print(f"Error querying data from map_info: {e}")
    finally:
        cursor.close()
    return map_id

def insert_log_info(connection, results):
    """
    将 log 信息插入到 log_info 表，并通过 filename 获取 map_id。
    """
    cursor = connection.cursor()
    for item in results:
        logfile = item["logfile"]
        date_captured = item["date_captured"]
        vehicle = item["vehicle"]
        map_id = get_map_id(connection, item["filename"])

        if map_id is None:
            continue  # 如果未找到匹配的 map_id，跳过该记录

        try:
            insert_query = """
            INSERT INTO log_info (log_name, log_date, map_id, vehicle_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (logfile, date_captured, map_id, vehicle))
        except mysql.connector.Error as e:
            print(f"Error inserting data into log_info: {e}")

    # 提交事务
    connection.commit()
    print("log_info 表数据成功插入！")
    cursor.close()

def process_data():
    """
    处理 map 和 log 的数据，生成去重后的结果。
    """
    results = []
    for map_item in nusc.map:
        for log_id in map_item["log_tokens"]:
            for log_item in nusc.log:
                if log_id == log_item["token"]:
                    results.append(
                        {
                            "category": map_item["category"],
                            "map_token": map_item["token"],
                            "filename": map_item["filename"],
                            "log_tokens": log_id,
                            "logfile": log_item["logfile"],
                            "vehicle": log_item["vehicle"],
                            "date_captured": log_item["date_captured"],
                            "location": log_item["location"],
                        }
                    )

    # 去重
    unique_results = []
    seen = set()
    for item in results:
        token_location_pair = (item["map_token"], item["location"])
        if token_location_pair not in seen:
            unique_results.append(item)
            seen.add(token_location_pair)

    return unique_results, results

def insert_map_log(connection):
    unique_results, results = process_data()
    # 插入 map_info 表数据
    insert_map_info(connection, unique_results)
    # 插入 log_info 表数据
    insert_log_info(connection, results)


# 查询log_id
def query_logid(connection,log_token):
    cursor = connection.cursor()

    try:
        # 定义查询SQL语句
        select_query = """
        SELECT log_info_id FROM log_info
        WHERE log_name = %s 
        """
        # 执行查询
        temp = nusc.get('log', log_token)

        cursor.execute(select_query, (temp["logfile"],))

        # 获取查询结果并检查是否存在
        result = cursor.fetchone()
        if result is None:
            print("未找到匹配的 log_id")

        log_id = result[0]

        print(log_id)
        return log_id
    except mysql.connector.Error as e:
        print(f"Error fetching or inserting data: {e}")

    # 提交事务
    connection.commit()
    # 关闭游标
    cursor.close()


# 插入category数据
def insert_category(connection):
    if connection is None:
        print("无法插入数据，因为数据库连接未成功建立。")
        return    
    cursor = connection.cursor()

    # 插入数据到category表
    for item in nusc.category:
        name = item["name"]
        description = item["description"]
        

        try:
            # 执行插入SQL语句
            insert_query = """
            INSERT INTO category_description (category_subcategory_name, category_description)
            VALUES (%s, %s)
            """
            cursor.execute(insert_query, (name, description))
        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")

    # 提交事务
    connection.commit()
    print("category成功插入！")
    cursor.close()

    
# 插入scene和sample
# 更新scene的frist、last、count属性
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

# 插入单个scene，frist、last、count为none，返回插入scene的自增主键
def insert_scene(connection,scene_item): 
    cursor = connection.cursor()
    # 插入一个空的scene
    description = scene_item["description"]
    log_info_id = query_logid(connection,scene_item["log_token"])
    try:
        # 执行插入SQL语句
        insert_query = """
        INSERT INTO scene_info (scene_description, log_info_id)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (description, log_info_id))
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
    # 提交事务
    connection.commit()
    return cursor.lastrowid

# 插入样本信息
def add_sample_info(conn, timestamp, scene_id=None, previous_sample_id=None, next_sample_id=None):
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

# 更新前一个样本的 next_sample_id
def update_next_sample_id(conn, current_id, prev_id):
    if prev_id:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sample_info SET next_sample_id = %s WHERE sample_id = %s",
            (current_id, prev_id)
        )
        conn.commit()

def insert_scene_sample(connection):
    for scene_item in nusc.scene:
        previous_sample_id = None
        first_sample_id = None
        scene_last_id = insert_scene(connection, scene_item)
        for sample_item in nusc.sample:
            if sample_item["scene_token"] == scene_item["token"]:
                second_timestamp = sample_item["timestamp"] / 1_000_000
                dt_object = datetime.datetime.fromtimestamp(second_timestamp)
                formatted_timestamp = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')
                sample_last_id = add_sample_info(connection,formatted_timestamp,scene_last_id,previous_sample_id)
                update_next_sample_id(connection, sample_last_id , previous_sample_id)
                previous_sample_id = sample_last_id
                if not first_sample_id:
                    first_sample_id = sample_last_id
                update_scene_info_sample(connection, scene_last_id,first_sample_id,previous_sample_id,increment_count=True)




if __name__ == '__main__':
    connectdatabase()
    if connection is not None and connection.is_connected():
        connection.close()