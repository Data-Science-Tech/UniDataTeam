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

        query_logid(connection,"6f7fe59adf984e55a82571ab4f17e4e2")

    
    except Error as e:
        print("数据库连接或操作失败：", e)

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("数据库连接已关闭")

def query_logid(connection,log_token):
    cursor = connection.cursor()

    try:
        # 定义查询SQL语句
        select_query = """
        SELECT log_info_id FROM log_info
        WHERE log_name = %s 
        """
        # 执行查询
        temp = nusc.get('log', log_token)

        cursor.execute(select_query, (temp["logfile"],))

        # 获取查询结果并检查是否存在
        result = cursor.fetchone()
        if result is None:
            print("未找到匹配的 log_id")

        log_id = result[0]

        print(log_id)
        return log_id
    except mysql.connector.Error as e:
        print(f"Error fetching or inserting data: {e}")

    # 提交事务
    connection.commit()
    # 关闭游标
    cursor.close()


if __name__ == '__main__':
    connectdatabase()
    if connection is not None and connection.is_connected():
        connection.close()