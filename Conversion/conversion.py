from nuscenes.nuscenes import NuScenes
import os
current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import mysql.connector
from mysql.connector import Error
import math

connection = None
nusc = NuScenes(version='v1.0-mini', dataroot=current_folder+'\\v1.0-mini', verbose=True)


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
        insert_category(connection)

    
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
def insert_map_log(connection):
    # map和log的笛卡尔积
    results = []
    for map_item in nusc.map:
        for log_id in map_item["log_tokens"]:
            for log_item in nusc.log:
                if log_id == log_item["token"]:
                    results.append(
                        {
                            "category":map_item["category"],
                            "map_token":map_item["token"],
                            "filename": map_item["filename"],
                            "log_tokens":log_id,
                            "logfile":log_item["logfile"],
                            "vehicle":log_item["vehicle"] ,
                            "date_captured":log_item["date_captured"] ,
                            "location": log_item["location"],
                        }
                    )
    # for result in results:
    #     print (result)
    # 用来保存去重后的结果
    unique_results = []
    # 用集合保存已见过的 (map_token, location) 组合
    seen = set()
    for item in results:
        # 获取当前项的 map_token 和 location
        token_location_pair = (item["map_token"], item["location"])
    
        # 检查是否已经遇到过这个组合
        if token_location_pair not in seen:
            # 如果没有见过，则添加到结果列表中并记录在 seen 集合中
            unique_results.append(item)
            seen.add(token_location_pair)

    # print("去重后的结果：", unique_results)
    # print(len(unique_results))

    if connection is None:
        print("无法插入数据，因为数据库连接未成功建立。")
        return    
    cursor1 = connection.cursor()

    # # 插入数据到map_info表
    # for item in unique_results:
    #     category = item["category"]
    #     filename = item["filename"]
    #     location = item["location"]

    #     try:
    #         # 执行插入SQL语句
    #         insert_query = """
    #         INSERT INTO map_info (location, filename, category)
    #         VALUES (%s, %s, %s)
    #         """
    #         cursor.execute(insert_query, (location, filename, category))
    #     except mysql.connector.Error as e:
    #         print(f"Error inserting data: {e}")
    # # 提交事务
    # connection.commit()
    # print("map_info成功插入！")
    # cursor.close()

    # 插入数据到log_info表
    for item in results:
        logfile = item["logfile"]
        date_captured = item["date_captured"]
        vehicle = item["vehicle"]

        map_id = ""
        try:
            # 定义查询SQL语句
            select_query = """
            SELECT map_id FROM map_info
            WHERE filename = %s
            """
            # 执行查询
            cursor2 = connection.cursor()
            cursor2.execute(select_query, (item['filename'],))
            # 获取查询结果并检查是否存在
            temp = cursor2.fetchone()
            if temp is None:
                print("未找到匹配的 map_id")
                continue  # 跳过本次循环
            map_id = int(temp[0])
        except mysql.connector.Error as e:
            print(f"Error query data: {e}")

        
        try:
            # 执行插入SQL语句
            insert_query = """
            INSERT INTO log_info (log_name, log_date, map_id,vehicle_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor1.execute(insert_query, (logfile, date_captured, map_id,vehicle))
        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
    # 提交事务
    connection.commit()
    print("log_info成功插入！")
    cursor1.close()

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


if __name__ == '__main__':
    connectdatabase()
    if connection is not None and connection.is_connected():
        connection.close()