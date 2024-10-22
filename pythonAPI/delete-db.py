import sqlite3
import os

# 获取当前 Python 文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在的目录
current_directory = os.path.dirname(current_file_path)
print("当前目录:", current_directory)

relative_db_folder = r'../database'

db_folder = os.path.join(current_directory, relative_db_folder)
db_path = os.path.join(db_folder, 'test_database.db')
print("数据库路径:", os.path.abspath(db_path))

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# 连接SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 获取所有表的名称
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# 遍历所有表并删除其内容
for table_name in tables:
    cursor.execute(f"DELETE FROM {table_name[0]};")
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name[0]}';")  # 重置自增ID序列

# 提交事务并关闭连接
conn.commit()
conn.close()
