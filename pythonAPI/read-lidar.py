import sqlite3
import os
import numpy as np
import open3d as o3d

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
        if image_resolution is not None and data_file_format == 'bin':
            print(f"Image/Binary Data Size: {len(image_resolution)} bytes")
            # 展示点云数据
            lidar_points = np.frombuffer(image_resolution, dtype=np.float32).reshape(-1, 4)  # 假设每个点有 x, y, z, intensity
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(lidar_points[:, :3])
            vis = o3d.visualization.Visualizer()
            vis.create_window(window_name=f"Sensor Data ID: {sensor_data_id} - LiDAR Point Cloud", width=800, height=600)
            vis.add_geometry(pcd)
            vis.poll_events()
            vis.update_renderer()
            vis.run()
            vis.destroy_window()
        else:
            print("No LiDAR Data Available or Data Format is not 'bin'")
        print("-" * 50)

# 调用函数读取所有传感器数据
read_all_sensor_data()

# 关闭连接
conn.close()
print("数据库连接已关闭。")
