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


class DatabaseDataset(Dataset):
    def __init__(self, db_config, scene_id, is_training=True):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.scene_id = scene_id
        self.is_training = is_training

        # 获取 scene_id
        self.cursor.execute("""SELECT scene_id FROM scene_info WHERE scene_id = %s""", (self.scene_id,))
        scene_id = self.cursor.fetchone()
        if scene_id:
            self.scene_id = scene_id[0]
        else:
            raise ValueError(f"Scene '{self.scene_id}' not found in database.")

        # 获取所有 sample_id
        self.cursor.execute("""SELECT sample_id FROM sample_info WHERE scene_id = %s""", (self.scene_id,))
        self.samples = [row[0] for row in self.cursor.fetchall()]

        # 获取 sensor_data 信息，过滤格式为 png 的数据
        self.data = []
        for sample_id in self.samples:
            self.cursor.execute("""
                SELECT sensor_data_id, file_path
                FROM sensor_data
                WHERE sample_id = %s AND data_file_format = 'png'
            """, (sample_id,))
            self.data.extend(self.cursor.fetchall())

        # 获取类别为 Car 的 category_description_id
        if self.is_training:
            self.cursor.execute("""SELECT category_description_id FROM category_description WHERE category_subcategory_name = 'Car'""")
            result = self.cursor.fetchone()
            if result:
                self.car_category_id = result[0]
            else:
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
        if self.is_training and self.car_category_id is not None:
            sample_id = self.samples[idx]

            # 查询类别为 Car 的标注
            self.cursor.execute("""
                SELECT sa.bbox_2d_xmin, sa.bbox_2d_ymin, sa.bbox_2d_xmax, sa.bbox_2d_ymax
                FROM sample_annotation sa
                JOIN instance i ON sa.instance_id = i.instance_id
                WHERE sa.sample_id = %s AND i.category_description_id = %s
            """, (sample_id, self.car_category_id))
            annotations = self.cursor.fetchall()

            # 转换为 (xmin, ymin, xmax, ymax) 格式
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
    parser.add_argument('--algorithm', type=str, required=True)
    parser.add_argument('--learning_rate', type=float, required=True)
    parser.add_argument('--num_epochs', type=int, required=True)
    parser.add_argument('--batch_size', type=int, required=True)
    parser.add_argument('--momentum', type=float, required=True)
    parser.add_argument('--weight_decay', type=float, required=True)
    parser.add_argument('--scene_id', type=str, required=True)
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
        'model_path': f'models/{args.algorithm}_{args.scene_id}.pth'
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
        torch.save(model.state_dict(), results['model_path'])

        print(json.dumps(results))
        return 0
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        return 1


if __name__ == '__main__':
    args = parse_args()
    sys.exit(train_model(args))
