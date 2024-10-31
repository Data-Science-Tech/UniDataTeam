import mysql.connector
import torch
import cv2
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.utils.data import Subset
import torchvision
from torchvision.transforms import functional as F
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
import torch.optim as optim
import matplotlib.pyplot as plt
import random

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Step 1: 从数据库中读取数据
class DatabaseDataset(Dataset):
    def __init__(self, db_config, log_info_id, is_training=True):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.log_info_id = log_info_id
        self.is_training = is_training

        # 获取 sensor_calibration_id 对应于给定的 log_info_id
        self.cursor.execute("""
            SELECT sensor_calibration_id FROM log_info WHERE log_info_id = %s
        """, (self.log_info_id,))
        result = self.cursor.fetchone()
        if result:
            self.sensor_calibration_id = result[0]
        else:
            raise ValueError("Invalid log_info_id provided")

        # 获取所有 sensor_data_id 和 BLOB 图像数据对应于 sensor_calibration_id
        self.cursor.execute("""
            SELECT sensor_data_id, image_resolution FROM sensor_data WHERE sensor_calibration_id = %s
        """, (self.sensor_calibration_id,))
        self.data = self.cursor.fetchall()

        if self.is_training:
            # 获取 "Car" 对应的 category_description_id（仅用于训练集，有标签数据）
            self.cursor.execute("""
                SELECT category_description_id FROM category_description WHERE category_subcategory_name = 'Car'
            """)
            result = self.cursor.fetchone()
            if result:
                self.car_category_id = result[0]
            else:
                self.car_category_id = None
        else:
            self.car_category_id = None

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sensor_data_id, image_blob = self.data[idx]

        # 将 BLOB 转换为图像
        np_img = np.frombuffer(image_blob, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 如果是训练集（有标签数据），查询与当前图像关联的标注
        if self.is_training and self.car_category_id is not None:
            self.cursor.execute("""
                SELECT 2d_box_xmin, 2d_box_xmax, 2d_box_ymin, 2d_box_ymax
                FROM sample_annotation
                JOIN sample_info ON sample_annotation.sample_id = sample_info.sample_id
                WHERE sample_info.sensor_data_id = %s AND category_description_id = %s
            """, (sensor_data_id, self.car_category_id))
            annotations = self.cursor.fetchall()

            # 转换为 (xmin, ymin, xmax, ymax) 格式
            boxes = []
            for annotation in annotations:
                xmin, xmax, ymin, ymax = annotation
                boxes.append([xmin, ymin, xmax, ymax])

            if len(boxes) == 0:
                boxes = torch.zeros((0, 4), dtype=torch.float32)
                labels = torch.zeros((0,), dtype=torch.int64)
            else:
                boxes = torch.as_tensor(boxes, dtype=torch.float32)
                labels = torch.ones((boxes.shape[0],), dtype=torch.int64)

            target = {'boxes': boxes, 'labels': labels}
            return F.to_tensor(image), target

        # 如果是测试集（没有标签数据），只返回图像
        else:
            return F.to_tensor(image), {}

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()

# 数据库连接配置
db_config = {
    'host': '122.51.133.37',
    'user': 'dev',
    'password': 'dev123',
    'database': 'car_perception_db'
}

dataset = DatabaseDataset(db_config, log_info_id=1, is_training=True)
dataloader = DataLoader(dataset, batch_size=4, shuffle=False, collate_fn=lambda x: tuple(zip(*x)))

# Step 2: 加载模型并训练
weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=weights)
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(in_features, num_classes=2)
model.to(device)

optimizer = optim.SGD(model.parameters(), lr=0.005, momentum=0.9, weight_decay=0.0005)
num_epochs = 10

model.train()
for epoch in range(num_epochs):
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

    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {epoch_loss / len(dataloader)}")

model_save_path = 'fasterrcnn_kitti_car_detector.pth'
torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")

# Step 3: 测试模型
test_dataset = DatabaseDataset(db_config, log_info_id=2, is_training=False)
test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False, collate_fn=lambda x: tuple(zip(*x)))

model.eval()
with torch.no_grad():
    for images, _ in test_dataloader:
        images = [img.to(device) for img in images]
        predictions = model(images)

        for i, prediction in enumerate(predictions):
            img = images[i].permute(1, 2, 0).cpu().numpy()
            img = (img * 255).astype(np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            boxes = prediction['boxes'].cpu().numpy()
            scores = prediction['scores'].cpu().numpy()

            for box, score in zip(boxes, scores):
                if score > 0:  # 降低阈值以显示更多检测结果
                    xmin, ymin, xmax, ymax = box
                    cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                    cv2.putText(img, f'{score:.2f}', (int(xmin), int(ymin) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(12, 8))
            plt.imshow(img)
            plt.axis('off')
            plt.show()

dataset.close()
test_dataset.close()
