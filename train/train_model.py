import argparse
import json
import sys
import torch
from torch.utils.data import DataLoader, Dataset, random_split
import cv2
import mysql.connector
from mysql.connector import pooling
import torchvision
from torchvision.transforms import functional as F
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights, ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
import os
from datetime import datetime
import time
from mysql.connector import Error
import random

script_path_parent = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists("datasets"):
    os.makedirs("datasets")
os.chdir("datasets") # 必须在datasets目录下运行，否则无法导入DatabaseDataset

base_dir = "/app/datasets"

# 数据库连接池配置
# DB_CONFIG = {
#     'pool_name': 'mypool',
#     'pool_size': 5,
#     'host': '122.51.133.37',
#     'user': 'dev',
#     'password': 'dev123',
#     'database': 'car_perception_db',
#     'connect_timeout': 86400,
#     'pool_reset_session': True,
#     'autocommit': True,
#     'get_warnings': True,
#     'raise_on_warnings': True,
#     'connection_timeout': 86400
# }
DB_CONFIG = {
    'pool_name': 'mypool',
    'pool_size': 5,
    'host': '100.80.142.150',
    'user': 'root',
    'password': 'root',
    'database': 'car_perception_db',
    'connect_timeout': 86400,
    'pool_reset_session': True,
    'autocommit': True,
    'get_warnings': True,
    'raise_on_warnings': True,
    'connection_timeout': 86400
}

def get_connection_from_pool():
    max_retries = 3
    retry_delay = 5  # 秒

    for attempt in range(max_retries):
        try:
            connection_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_CONFIG)
            return connection_pool.get_connection()
        except Error as err:
            if attempt == max_retries - 1:  # 最后一次尝试
                raise
            print(f"数据库连接失败，{retry_delay}秒后重试: {err}")
            time.sleep(retry_delay)

class DatabaseDataset(Dataset):
    def __init__(self, scene_ids, is_training=True):
        self.is_training = is_training
        self.scene_ids = [int(id) for id in scene_ids.split(',')]
        self.conn = get_connection_from_pool()
        self.cursor = self.conn.cursor()

        try:
            # 验证所有场景ID
            scene_id_str = ','.join(map(str, self.scene_ids))
            self.cursor.execute(f"""  
                SELECT scene_id FROM scene_info   
                WHERE scene_id IN ({scene_id_str})  
            """)
            found_scenes = self.cursor.fetchall()
            if len(found_scenes) != len(self.scene_ids):
                raise ValueError(f"Some scenes not found in database")

            # 获取所有指定场景的sample_id
            self.cursor.execute(f"""  
                SELECT sample_id FROM sample_info   
                WHERE scene_id IN ({scene_id_str})  
            """)
            self.samples = [row[0] for row in self.cursor.fetchall()]

            # 获取sensor_data信息
            self.data = []
            for sample_id in self.samples:
                self.cursor.execute("""  
                    SELECT sensor_data_id, file_path  
                    FROM sensor_data  
                    WHERE sample_id = %s AND (data_file_format = 'jpg' OR data_file_format = 'png' OR data_file_format = 'jpeg')  
                """, (sample_id,))
                self.data.extend(self.cursor.fetchall())

            if self.is_training:
                self.cursor.execute("""SELECT category_description_id FROM category_description WHERE   
                category_subcategory_name = 'Car' OR category_subcategory_name LIKE 'vehicle%'""")
                results = self.cursor.fetchall()
                self.car_category_ids = [result[0] for result in results]
                if not self.car_category_ids:
                    raise ValueError("Category 'Car' not found in database.")
            else:
                self.car_category_id = None

        except Error as err:
            self.close()
            raise err

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        try:
            if not self.conn.is_connected():
                self.conn = get_connection_from_pool()
                self.cursor = self.conn.cursor()

            sensor_data_id, file_path = self.data[idx]

            # 读取图像
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Failed to load image from path: {file_path}")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # 如果是训练集，获取标注
            if self.is_training and self.car_category_ids is not None:
                sensor_data_id = self.data[idx][0]

                self.cursor.execute("""  
                SELECT a2d.bbox_2d_xmin, a2d.bbox_2d_ymin, a2d.bbox_2d_xmax, a2d.bbox_2d_ymax  
                FROM sensor_data sd  
                JOIN annotation_2d a2d ON sd.sensor_data_id = a2d.sensor_data_id  
                JOIN sample_annotation sa ON a2d.sample_annotation_id = sa.annotation_id  
                JOIN instance i ON sa.instance_id = i.instance_id  
                WHERE sd.sensor_data_id = %s   
                AND i.category_description_id IN (%s)  
                """ % (sensor_data_id, ','.join(map(str, self.car_category_ids))))
                annotations = self.cursor.fetchall()

                boxes = [list(annotation) for annotation in annotations]
                if len(boxes) == 0:
                    boxes = torch.zeros((0, 4), dtype=torch.float32)
                    labels = torch.zeros((0,), dtype=torch.int64)
                else:
                    boxes = torch.as_tensor(boxes, dtype=torch.float32)
                    labels = torch.ones((boxes.shape[0],), dtype=torch.int64)

                target = {'boxes': boxes, 'labels': labels}
                return F.to_tensor(image), target
            else:
                return F.to_tensor(image), {}

        except Error as err:
            print(f"Database error in __getitem__: {err}")
            if not self.conn.is_connected():
                self.conn = get_connection_from_pool()
                self.cursor = self.conn.cursor()
            raise err

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_config_id', type=int, required=True)
    parser.add_argument('--algorithm', type=str, default='FAST_R_CNN')
    parser.add_argument('--learning_rate', type=float,  default=0.005)
    parser.add_argument('--num_epochs', type=int, default=10)
    parser.add_argument('--batch_size', type=int, default=4)
    parser.add_argument('--momentum', type=float, default=0.9)
    parser.add_argument('--weight_decay', type=float, default=5e-4)
    parser.add_argument('--scene_ids', type=str, required=True,
                        help='Comma-separated list of scene IDs')
    parser.add_argument('--val_split', type=float, default=0.2,
                        help='Proportion of dataset to use for validation (default: 0.2)')
    return parser.parse_args()

def create_faster_rcnn_model():
    weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=weights)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(in_features, num_classes=2)
    return model

def create_ssd_model():
    weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
    model = ssdlite320_mobilenet_v3_large(weights=weights)
    return model

def compute_iou(box1, box2):
    """
    Compute Intersection over Union (IoU) between two boxes.
    box: [xmin, ymin, xmax, ymax]
    """
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    box1Area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2Area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    iou = interArea / float(box1Area + box2Area - interArea)
    return iou

def evaluate_model(model, dataloader, device, iou_threshold=0.5):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, targets in dataloader:
            images = [img.to(device) for img in images]
            outputs = model(images)

            for output, target in zip(outputs, targets):
                pred_boxes = output['boxes'].cpu().numpy()
                pred_labels = output['labels'].cpu().numpy()
                pred_scores = output['scores'].cpu().numpy()

                gt_boxes = target['boxes'].numpy()
                gt_labels = target['labels'].numpy()

                # For simplicity, match each ground truth box with the highest scoring prediction
                for gt_box, gt_label in zip(gt_boxes, gt_labels):
                    matched = False
                    for pred_box, pred_label, pred_score in zip(pred_boxes, pred_labels, pred_scores):
                        if pred_label == gt_label:
                            iou = compute_iou(gt_box, pred_box)
                            if iou >= iou_threshold:
                                matched = True
                                break
                    if matched:
                        correct += 1
                    total += 1

    accuracy = correct / total if total > 0 else 0
    return accuracy

def train_epoch(model, dataloader, optimizer, device, epoch, total_epochs):
    epoch_loss = 0
    # 获取数据加载器的总批次数
    total_batches = len(dataloader)

    for batch_idx, (images, targets) in enumerate(dataloader):
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        if any(len(t['boxes']) == 0 for t in targets):
            continue

        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        # 累计损失
        current_loss = losses.item()
        epoch_loss += current_loss

        # 计算当前批次的平均损失
        avg_loss = epoch_loss / (batch_idx + 1)

        # 输出进度信息
        progress = {
            "type": "progress",
            "current_epoch": epoch + 1,
            "total_epochs": total_epochs,
            "current_batch": batch_idx + 1,
            "total_batches": total_batches,
            "current_loss": current_loss,
            "avg_loss": avg_loss,
            "progress_percentage": ((epoch * total_batches + batch_idx + 1) / (total_epochs * total_batches)) * 100
        }

        # 使用特定前缀输出进度信息
        print(f"PROGRESS:{json.dumps(progress)}", flush=True)

    # 计算整个epoch的平均损失
    epoch_avg_loss = epoch_loss / len(dataloader)

    # 输出epoch完成信息
    epoch_progress = {
        "type": "epoch_complete",
        "epoch": epoch + 1,
        "total_epochs": total_epochs,
        "epoch_loss": epoch_avg_loss,
        "progress_percentage": ((epoch + 1) / total_epochs) * 100
    }
    print(f"PROGRESS:{json.dumps(epoch_progress)}", flush=True)

    return epoch_avg_loss

def train_model(args):
    start_time = datetime.now()
    conn = get_connection_from_pool()
    cursor = conn.cursor()

    try:
        # Define base directory and relative paths
        # base_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_path_parent)))
        results_dir = os.path.join(base_dir, 'files', 'models')
        logs_dir = os.path.join(base_dir, 'files', 'train_logs')

        # Create directories if they don't exist
        os.makedirs(results_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)

        # Store relative paths for database
        scene_id_str = args.scene_ids.replace(',', '_')
        relative_model_path = os.path.join('files', 'models',
                                           f'{args.algorithm}_scenes_{scene_id_str}.pth')
        relative_log_path = os.path.join('files', 'train_logs',
                                         f'training_log_{args.algorithm}_scenes_{scene_id_str}.json')

        # Full paths for actual file operations
        model_path = os.path.join(base_dir, relative_model_path)
        log_path = os.path.join(base_dir, relative_log_path)

        # 验证model_config
        cursor.execute("""  
                SELECT id FROM model_config   
                WHERE id = %s  
            """, (args.model_config_id,))

        model_config = cursor.fetchone()
        if not model_config:
            raise ValueError(f"Model config with ID {args.model_config_id} not found")

        model_config_id = model_config[0]

        # 插入训练结果
        cursor.execute("""  
                INSERT INTO training_result (model_config_id, start_time, model_file_path)  
                VALUES (%s, %s, %s)  
            """, (model_config_id, start_time, relative_model_path))

        training_result_id = cursor.lastrowid
        conn.commit()

        # Create dataset
        full_dataset = DatabaseDataset(scene_ids=args.scene_ids, is_training=True)
        dataset_size = len(full_dataset)
        val_size = int(args.val_split * dataset_size)
        train_size = dataset_size - val_size

        train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size],
                                                  generator=torch.Generator().manual_seed(42))

        dataloader = DataLoader(train_dataset, batch_size=args.batch_size,
                                shuffle=True, collate_fn=lambda x: tuple(zip(*x)))

        val_dataloader = DataLoader(val_dataset, batch_size=args.batch_size,
                                    shuffle=False, collate_fn=lambda x: tuple(zip(*x)))

        # Initialize model
        if args.algorithm == 'FAST_R_CNN':
            model = create_faster_rcnn_model()
        elif args.algorithm == 'SSD':
            model = create_ssd_model()
        else:
            raise ValueError(f"Unsupported algorithm: {args.algorithm}")

        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        model.to(device)

        optimizer = torch.optim.SGD(model.parameters(),
                                    lr=args.learning_rate,
                                    momentum=args.momentum,
                                    weight_decay=args.weight_decay)

        results = {
            'training_result_id': training_result_id,
            'epoch_losses': [],
            'final_loss': 0,
            'accuracy': 0.0,
            'model_path': relative_model_path
        }

        # 计算总训练步数
        total_steps = args.num_epochs * len(dataloader)
        current_step = 0

        model.train()
        for epoch in range(args.num_epochs):
            epoch_loss = train_epoch(model, dataloader, optimizer, device, epoch, args.num_epochs)
            results['epoch_losses'].append(epoch_loss)

        # 评估模型
        accuracy = evaluate_model(model, val_dataloader, device)
        results['accuracy'] = accuracy

        # 输出训练完成信息
        completion_info = {
            "type": "complete",
            "final_loss": results['epoch_losses'][-1],
            "accuracy": results['accuracy'],
            "training_time": str(datetime.now() - start_time)
        }
        print(f"PROGRESS:{json.dumps(completion_info)}", flush=True)

        if not conn.is_connected():
            conn = get_connection_from_pool()
            cursor = conn.cursor()

        results['final_loss'] = results['epoch_losses'][-1]

        try:
            torch.save(model.state_dict(), model_path)
        except Exception as e:
            print(json.dumps({'error': f"Error saving model: {str(e)}"}))
            return 1

        end_time = datetime.now()
        # Write results
        try:
            with open(log_path, 'w') as log_file:
                json.dump(results, log_file, indent=4)
        except Exception as e:
            print(json.dumps({'error': f"Error saving log file: {str(e)}"}))
            return 1

        # 更新数据库，使用重试机制
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                if not conn.is_connected():
                    conn = get_connection_from_pool()
                    cursor = conn.cursor()

                end_time = datetime.now()
                cursor.execute("""  
                    UPDATE training_result  
                    SET end_time = %s, training_logs = %s, final_loss = %s, accuracy = %s
                    WHERE id = %s  
                """, (end_time, relative_log_path, results['final_loss'], results['accuracy'], training_result_id))
                conn.commit()
                break
            except Error as err:
                retry_count += 1
                if retry_count == max_retries:
                    print(json.dumps({'error': f"Failed to update database after {max_retries} attempts: {str(err)}"}))
                    return 1
                print(json.dumps({'warning': f"Database update attempt {retry_count} failed, retrying..."}))
                time.sleep(2)  # 等待2秒后重试

        print(json.dumps(results))
        return 0

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        return 1

    finally:
        try:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        except Error:
            pass  # 忽略关闭连接时的错误

if __name__ == '__main__':
    if torch.cuda.is_available():
        print("Using GPU")
    else:
        print("Using CPU")
    args = parse_args()
    sys.exit(train_model(args))
