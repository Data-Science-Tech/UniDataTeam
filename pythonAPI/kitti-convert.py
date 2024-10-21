import sqlite3
import os
import platform

system = platform.system()

# 获取当前 Python 文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在的目录
current_directory = os.path.dirname(current_file_path)

print("当前目录:", current_directory)

# 1. 设置数据库路径，并确保路径中的文件夹存在

relative_db_folder = r'../database'

db_folder = os.path.join(current_directory, relative_db_folder)

db_path = os.path.join(db_folder, 'test_database.db')

print("数据库路径:", os.path.abspath(db_path))

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# 创建并连接到 SQLite 数据库（如果不存在则会创建）
conn = sqlite3.connect(db_path)

# 创建一个游标对象，来执行 SQL 语句
cursor = conn.cursor()


# 提交更改
conn.commit()


# 5. 关闭连接
conn.close()
