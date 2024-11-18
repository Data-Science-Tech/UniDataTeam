import argparse
import json
import sys
import torch
from torch.utils.data import DataLoader, Dataset
import cv2
import mysql.connector
import torchvision
from torchvision.transforms import functional as F
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights, ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
import os
from datetime import datetime

script_path_parent = os.path.dirname(os.path.abspath(__file__))

class DatabaseDataset(Dataset):
    def __init__(self, db_config, scene_id, is_training=True):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.scene_id = scene_id
        self.is_training = is_training

        # 获取scene_id
        self.cursor.execute("""SELECT scene_id FROM scene_info WHERE scene_id = %s""", (self.scene_id,))
        scene_id = self.cursor.fetchone()
        if scene_id:
            self.scene_id = scene_id[0]
        else:
            raise ValueError(f"Scene '{self.scene_id}' not found in database.")

            # 获取所有sample_id
        self.cursor.execute("""SELECT sample_id FROM sample_info WHERE scene_id = %s""", (self.scene_id,))
        self.samples = [row[0] for row in self.cursor.fetchall()]

        # 获取sensor_data 信息，过滤格式为png 的数据
        self.data = []
        for sample_id in self.samples:
            self.cursor.execute("""  
                SELECT sensor_data_id, file_path  
                FROM sensor_data  
                WHERE sample_id = %s AND (data_file_format = 'jpg' OR data_file_format = 'png' OR data_file_format = 'jpeg')
            """, (sample_id,))
            self.data.extend(self.cursor.fetchall())

            # 获取类别为Car的category_description_id
        if self.is_training:
            self.cursor.execute("""SELECT category_description_id FROM category_description WHERE category_subcategory_name = 'Car'""")
            results = self.cursor.fetchall()
            self.car_category_ids = [result[0] for result in results]
            if not self.car_category_ids:
                raise ValueError("Category 'Car' not found in database.")
        else:
            self.car_category_id = None

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sensor_data_id, file_path = self.data[idx]

        # 读取图像
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Failed to load image from path: {file_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 如果是训练集，获取标注
        if self.is_training and self.car_category_ids is not None:
            sensor_data_id = self.data[idx][0]

            # 查询所有 car category ids 对应的标注
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

            # 转换为(xmin, ymin, xmax, ymax)格式
            boxes = [list(annotation) for annotation in annotations]
            if len(boxes) == 0:
                boxes = torch.zeros((0, 4), dtype=torch.float32)
                labels = torch.zeros((0,), dtype=torch.int64)
            else:
                boxes = torch.as_tensor(boxes, dtype=torch.float32)
                labels = torch.ones((boxes.shape[0],), dtype=torch.int64)

            target = {'boxes': boxes, 'labels': labels}
            return F.to_tensor(image), target

            # 测试集没有标注
        else:
            return F.to_tensor(image), {}

    def close(self):
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
    parser.add_argument('--scene_id', type=str, default=1)
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


def train_epoch(model, dataloader, optimizer, device):
    epoch_loss = 0
    for images, targets in dataloader:
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        if any(len(t['boxes']) == 0 for t in targets):
            continue  # 跳过没有标注的样本

        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        epoch_loss += losses.item()

    return epoch_loss / len(dataloader)


def train_model(args):
    # Database configuration
    db_config = {
        'host': '122.51.133.37',
        'user': 'dev',
        'password': 'dev123',
        'database': 'car_perception_db'
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    start_time = datetime.now()

    # Define base directory and relative paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_path_parent)))  # go up to springbootquickstart
    results_dir = os.path.join(base_dir, 'files', 'models')
    logs_dir = os.path.join(base_dir, 'files', 'train_logs')

    # Create directories if they don't exist
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    # Store relative paths for database
    relative_model_path = os.path.join('files', 'models', f'{args.algorithm}_{args.scene_id}.pth')
    relative_log_path = os.path.join('files', 'train_logs', f'training_log_{args.algorithm}_{args.scene_id}.json')

    # Full paths for actual file operations
    model_path = os.path.join(base_dir, relative_model_path)
    log_path = os.path.join(base_dir, relative_log_path)

    # 首先验证 model_config 是否存在
    cursor.execute("""  
            SELECT id FROM model_config   
            WHERE id = %s  
        """, (args.model_config_id,))  # 假设从参数中获取 model_config_id

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
    dataset = DatabaseDataset(db_config, scene_id=args.scene_id, is_training=True)
    dataloader = DataLoader(dataset, batch_size=args.batch_size,
                            shuffle=True, collate_fn=lambda x: tuple(zip(*x)))

    # Initialize model based on algorithm choice
    if args.algorithm == 'FAST_R_CNN':
        model = create_faster_rcnn_model()
    elif args.algorithm == 'SSD':
        model = create_ssd_model()
    else:
        raise ValueError(f"Unsupported algorithm: {args.algorithm}")

        # Training loop
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model.to(device)

    optimizer = torch.optim.SGD(model.parameters(),
                                lr=args.learning_rate,
                                momentum=args.momentum,
                                weight_decay=args.weight_decay)

    results = {
        'epoch_losses': [],
        'final_loss': 0,
        'model_path': relative_model_path
    }

    try:
        model.train()
        for epoch in range(args.num_epochs):
            epoch_loss = train_epoch(model, dataloader, optimizer, device)
            results['epoch_losses'].append(epoch_loss)
            print(json.dumps({
                'epoch': epoch + 1,
                'loss': epoch_loss
            }))

        results['final_loss'] = results['epoch_losses'][-1]
        torch.save(model.state_dict(), model_path)

        end_time = datetime.now()
        # Write results as a log file
        with open(log_path, 'w') as log_file:
            json.dump(results, log_file, indent=4)

            # Update training_result with final details
        cursor.execute("""  
            UPDATE training_result  
            SET end_time = %s, training_logs = %s, final_loss = %s  
            WHERE id = %s  
        """, (end_time, relative_log_path, results['final_loss'], training_result_id))
        conn.commit()

        print(json.dumps(results))
        return 0

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        return 1

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    if torch.cuda.is_available():
        print("Using GPU")
    else:
        print("Using CPU")
    args = parse_args()
    sys.exit(train_model(args))
