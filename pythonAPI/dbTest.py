import sqlite3
import os

# 1. 设置数据库路径，并确保路径中的文件夹存在
db_folder = r'C:\Users\uncle\_git-clones\Uni-DataTeam\database'
db_path = os.path.join(db_folder, 'test_database.db')

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# 创建并连接到 SQLite 数据库（如果不存在则会创建）
conn = sqlite3.connect(db_path)

# 创建一个游标对象，来执行 SQL 语句
cursor = conn.cursor()

# 2. 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

# 3. 插入数据
cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))

# 提交更改
conn.commit()

# 4. 查询数据
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

# 输出查询结果
for row in rows:
    print(row)

# 5. 关闭连接
conn.close()
