import sqlite3
import os
import cv2
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

# 获取当前 Python 文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在的目录
current_directory = os.path.dirname(current_file_path)
print("当前目录:", current_directory)

relative_db_folder = r'../database'

db_folder = os.path.join(current_directory, relative_db_folder)
db_path = os.path.join(db_folder, 'test_database.db')
print("数据库路径:", os.path.abspath(db_path))

# 连接SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询并读取所有传感器数据
def read_all_sensor_data():
    cursor.execute("SELECT sensor_data_id, timestamp, sensor_calibration_id, data_file_format, image_resolution FROM sensor_data")
    rows = cursor.fetchall()
    
    for row in rows:
        sensor_data_id, timestamp, sensor_calibration_id, data_file_format, image_resolution = row
        print(f"Sensor Data ID: {sensor_data_id}")
        print(f"Timestamp: {timestamp}")
        print(f"Sensor Calibration ID: {sensor_calibration_id}")
        print(f"Data File Format: {data_file_format}")
        if image_resolution is not None:
            print(f"Image/Binary Data Size: {len(image_resolution)} bytes")
            if data_file_format == 'png':
                # 展示图像数据
                nparr = np.frombuffer(image_resolution, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img is not None:
                    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    plt.title(f"Sensor Data ID: {sensor_data_id} - RGB Image")
                    plt.axis('off')
                    plt.show()
            elif data_file_format == 'bin':
                # 展示点云数据
                lidar_points = np.frombuffer(image_resolution, dtype=np.float32).reshape(-1, 4)  # 假设每个点有 x, y, z, intensity
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(lidar_points[:, :3])
                o3d.visualization.draw_geometries([pcd], window_name=f"Sensor Data ID: {sensor_data_id} - LiDAR Point Cloud")
        else:
            print("No Image/Binary Data Available")
        print("-" * 50)

# 调用函数读取所有传感器数据
read_all_sensor_data()

# 关闭连接
conn.close()
print("数据库连接已关闭。")
