import mysql.connector
import cv2

# 数据库连接信息
db_config = {
    'host': 'localhost',         # 数据库主机
    'user': 'root',         # 数据库用户名
    'password': 'root', # 数据库密码
    'database': 'car_perception_db'  # 数据库名
}

def get_rgb_images(scene_id):
    """
    获取指定 scene 的所有 RGB 图像文件路径和数据
    """
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 查询与 scene_id 关联的 RGB 图像数据
        query = """
        SELECT 
            sd.file_path, sd.image_width, sd.image_height 
        FROM 
            sensor_data sd
        JOIN 
            sample_info si ON sd.sample_id = si.sample_id
        WHERE 
            si.scene_id = %s AND sd.data_file_format = 'jpg' AND sd.image_width IS NOT NULL;
        """
        cursor.execute(query, (scene_id,))
        result = cursor.fetchall()

        return result

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def display_images(image_data_list):
    """
    读取并显示图像
    """
    for image_data in image_data_list:
        file_path = image_data['file_path']

        # 读取图像
        image = cv2.imread(file_path)
        if image is None:
            print(f"无法读取图像: {file_path}")
            continue

        # 显示图像
        cv2.imshow(f"Image: {file_path}", image)

        # 等待用户按键（按 'q' 退出）
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    # 销毁所有窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 替换为你要查询的 scene_id
    scene_id = 1  # 示例 Scene ID

    # 获取场景的所有 RGB 图像数据
    images = get_rgb_images(scene_id)
    if not images:
        print("没有找到任何图像数据。")
    else:
        print(f"找到 {len(images)} 张图像，开始显示...")

        # 显示图像
        display_images(images)
