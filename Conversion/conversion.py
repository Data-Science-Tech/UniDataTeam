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
        insert_sensor_calibration(connection)

    
    except Error as e:
        print("数据库连接或操作失败：", e)

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("数据库连接已关闭")




# 插入传感器数据
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
    print("成功插入！")
    cursor.close()


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
    # calibrated_sensor
    for item in nusc.calibrated_sensor:
        # print(nusc.get('sensor', item["sensor_token"]))

        try:
            # 定义查询SQL语句
            select_query = """
            SELECT sensor_id FROM sensor
            WHERE sensor_type = %s AND sensor_name = %s
            """
            temp=nusc.get('sensor', item["sensor_token"])
            # 执行查询
            cursor.execute(select_query, (temp['channel'], temp['modality']))

            # 获取查询结果
            result = cursor.fetchone()
            # sensor_id = result[0]

            

        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
        


if __name__ == '__main__':
    connectdatabase()
    if connection is not None and connection.is_connected():
        connection.close()