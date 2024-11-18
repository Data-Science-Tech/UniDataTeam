import mysql.connector

# 数据库配置
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

# 要清空的表列表
tables_to_truncate = [
    "annotation_2d",
    "annotation_attribute",
    "attribute",
    "category_description",
    "instance",
    "log_info",
    "map_info",
    "model_config",
    "nuscene_token_to_id",
    "sample_annotation",
    "sample_info",
    "scene_info",
    "semantic_segmentation",
    "sensor",
    "sensor_calibration",
    "sensor_data",
    "training_result"
]

def clear_tables(cursor):
    """
    清空所有指定表的数据并重置 AUTO_INCREMENT
    """
    # 禁用外键约束
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    print("Foreign key checks disabled.")

    # 遍历表并清空数据
    for table in tables_to_truncate:
        try:
            cursor.execute(f"TRUNCATE TABLE {table};")
            print(f"Table {table} truncated successfully.")
        except Exception as e:
            print(f"Failed to truncate table {table}: {e}")

    # 启用外键约束
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("Foreign key checks enabled.")

def main():
    # 连接数据库
    connection = mysql.connector.connect(**local_db_config)
    cursor = connection.cursor()

    try:
        # 清空表数据
        clear_tables(cursor)

        # 提交更改
        connection.commit()
        print("All tables cleared and reset successfully.")

    except Exception as e:
        # 处理错误并回滚
        connection.rollback()
        print(f"Error occurred: {e}")

    finally:
        # 关闭数据库连接
        cursor.close()
        connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
