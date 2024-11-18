import mysql.connector
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# 数据库配置
local_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'car_perception_db'
}

def fetch_annotations_and_images(scene_id):
    try:
        # 连接到数据库
        connection = mysql.connector.connect(**local_db_config)
        cursor = connection.cursor(dictionary=True)

        # 查询 2D 标注数据和图片路径
        query = """
            SELECT 
                a.annotation_2d_id,
                a.bbox_2d_xmin,
                a.bbox_2d_xmax,
                a.bbox_2d_ymin,
                a.bbox_2d_ymax,
                sd.file_path
            FROM annotation_2d AS a
            INNER JOIN sensor_data AS sd ON a.sensor_data_id = sd.sensor_data_id
            INNER JOIN sample_info AS s ON sd.sample_id = s.sample_id
            WHERE s.scene_id = %s;
        """
        
        cursor.execute(query, (scene_id,))
        results = cursor.fetchall()
        return results
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def visualize_annotations(annotations):
    for annotation in annotations:
        try:
            # 加载对应图片
            rootDir = r"D:\datasets\nuScenes\v1.0-mini\\"
            image = Image.open(rootDir + annotation['file_path'])
            draw = ImageDraw.Draw(image)

            # 绘制 2D 标注框
            bbox = [
                annotation['bbox_2d_xmin'],
                annotation['bbox_2d_ymin'],
                annotation['bbox_2d_xmax'],
                annotation['bbox_2d_ymax']
            ]
            draw.rectangle(bbox, outline="red", width=3)

            # 使用 Matplotlib 显示图片
            plt.figure(figsize=(8, 6))
            plt.imshow(image)
            plt.title(f"Annotation ID: {annotation['annotation_2d_id']}")
            plt.axis("off")
            plt.show()
        
        except FileNotFoundError:
            print(f"Image not found: {annotation['file_path']}")
        except Exception as e:
            print(f"Error visualizing annotation: {e}")

# 示例调用
scene_id = 1  # 替换为实际场景 ID
annotations = fetch_annotations_and_images(scene_id)
if annotations:
    visualize_annotations(annotations)
else:
    print("No annotations found for the specified scene.")
