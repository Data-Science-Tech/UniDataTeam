import mysql.connector

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'car_perception_db'
}

# Debug 模式开关
DEBUG_MODE = True  # 设置为 True 开启调试信息，设置为 False 禁用调试信息

def debug_print(message):
    """
    打印调试信息，仅在 DEBUG_MODE 为 True 时生效
    :param message: 要打印的调试信息
    """
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")

def get_or_create_mapping(cursor, token, source_table, target_table, id_column):
    """
    获取或生成一个表（如 scene 表）中主键 ID 对应的 token 映射。
    :param cursor: MySQL 数据库游标
    :param token: nuScenes 的 token (字符串)
    :param source_table: 映射表的名称（如 nuscene_token_to_id）
    :param target_table: 目标表的名称（如 scene 表）
    :param id_column: 目标表的主键列名称（如 scene_id）
    :return: 返回映射的 ID
    """
    # 1. 检查映射表中是否存在 token 映射
    query = f"""
    SELECT id FROM {source_table}
    WHERE token = %s AND source_table = %s
    """
    cursor.execute(query, (token, target_table))
    result = cursor.fetchone()

    if result:
        # 如果映射已存在，返回对应的 ID
        debug_print(f"Found existing mapping: token={token}, source_table={target_table}, id={result[0]}")
        return result[0]

    debug_print(f"No mapping found for token={token}, source_table={target_table}")

    # 2. 查询映射表中当前 source_table 的最大 ID
    max_mapping_id_query = f"""
    SELECT MAX(id) FROM {source_table}
    WHERE source_table = %s
    """
    cursor.execute(max_mapping_id_query, (target_table,))
    max_mapping_id_result = cursor.fetchone()
    max_mapping_id = max_mapping_id_result[0] if max_mapping_id_result and max_mapping_id_result[0] else 0

    debug_print(f"Current max ID in source_table={source_table} for source_table={target_table}: {max_mapping_id}")

    # 3. 查询目标表中的最大 ID
    max_id_query = f"SELECT MAX({id_column}) FROM {target_table}"
    cursor.execute(max_id_query)
    max_id_result = cursor.fetchone()
    max_id = max_id_result[0] if max_id_result and max_id_result[0] else 0

    debug_print(f"Current max ID in target_table={target_table}, id_column={id_column}: {max_id}")

    # 4. 生成新的 ID，取映射表和目标表中的最大 ID
    new_id = max(max_mapping_id, max_id) + 1
    debug_print(f"Generated new ID: {new_id}")

    # 5. 插入新的映射到映射表
    insert_query = f"""
    INSERT INTO {source_table} (token, source_table, id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (token, target_table, new_id))
    debug_print(f"Inserted new mapping: token={token}, source_table={target_table}, id={new_id}")
    debug_print("\n")

    return new_id

def insert_scene_info(cursor, scene_id, description, log_id, sample_count, first_sample_id, last_sample_id):
    """
    插入一条 scene 信息到 scene_info 表中
    """
    sql = """
    INSERT INTO scene_info (scene_id, scene_description, log_info_id, sample_count, first_sample_id, last_sample_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (scene_id, description, log_id, sample_count, first_sample_id, last_sample_id)
    cursor.execute(sql, data)

def main():
    # 连接到数据库
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # 加载 nuScenes 数据集
    from nuscenes.nuscenes import NuScenes
    nusc = NuScenes(version='v1.0-mini', dataroot=r'D:\datasets\nuScenes\v1.0-mini', verbose=True)

    try:
        # 禁用外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        debug_print("Foreign key checks disabled.")

        # 开始事务
        connection.start_transaction()

        # 遍历所有 scene 并插入到数据库
        for scene in nusc.scene:
            # 获取或生成映射
            scene_id = get_or_create_mapping(cursor, scene['token'], 'nuscene_token_to_id', 'scene_info', 'scene_id')
            log_id = get_or_create_mapping(cursor, scene['log_token'], 'nuscene_token_to_id', 'log_info', 'log_info_id')
            first_sample_id = get_or_create_mapping(cursor, scene['first_sample_token'], 'nuscene_token_to_id', 'sample_info', 'sample_id')
            last_sample_id = get_or_create_mapping(cursor, scene['last_sample_token'], 'nuscene_token_to_id', 'sample_info', 'sample_id')

            # 提取其他字段
            description = scene['description']
            sample_count = scene['nbr_samples']

            # 插入 scene_info 数据
            insert_scene_info(cursor, scene_id, description, log_id, sample_count, first_sample_id, last_sample_id)

        # 提交事务
        connection.commit()
        debug_print("Transaction committed successfully.")

    except Exception as e:
        # 如果发生错误，回滚事务
        connection.rollback()
        debug_print(f"Transaction rolled back due to error: {e}")

    finally:
        # 恢复外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        debug_print("Foreign key checks enabled.")

        # 关闭数据库连接
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
