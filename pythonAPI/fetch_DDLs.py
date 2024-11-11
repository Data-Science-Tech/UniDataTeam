import mysql.connector

# 数据库连接配置
remote_db_config = {
    'host': '122.51.133.37',
    'user': 'dev',
    'password': 'dev123',
    'database': 'car_perception_db'
}

local_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'car_perception_db'
}


# 创建数据库连接
connection = mysql.connector.connect(**local_db_config)
cursor = connection.cursor()

try:
    # 获取所有表名
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    # 打开文件以保存所有 DDL
    with open("all_tables_ddl.txt", "w", encoding="utf-8") as ddl_file:
        for table in tables:
            table_name = table[0]
            
            # 获取表的 DDL
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`;")
            ddl_result = cursor.fetchone()
            ddl = ddl_result[1]
            
            # 写入文件
            ddl_file.write(f"-- DDL for table: {table_name}\n")
            ddl_file.write(f"{ddl};\n\n")
        
    print("所有表的DDL已导出到 all_tables_ddl.txt 文件中。")

except mysql.connector.Error as err:
    print(f"错误: {err}")
finally:
    cursor.close()
    connection.close()
