import sqlite3
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
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # 获取 "Car" 对应的 category_description_id
        self.cursor.execute("""
            SELECT category_description_id FROM category_description WHERE category_subcategory_name = 'Car'
        """)
        result = self.cursor.fetchone()
        if result:
            self.car_category_id = result[0]
        else:
            raise ValueError("Database does not contain a 'Car' category")

        # 获取所有 sensor_data_id 和 BLOB 图像数据
        self.cursor.execute("SELECT sensor_data_id, image_resolution FROM sensor_data")
        self.data = self.cursor.fetchall()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sensor_data_id, image_blob = self.data[idx]

        # 将 BLOB 转换为图像
        np_img = np.frombuffer(image_blob, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 查询与当前图像关联的标注
        self.cursor.execute("""
            SELECT coordinates
            FROM sample_annotation 
            WHERE sample_id = ? AND category_description_id = ?
        """, (sensor_data_id, self.car_category_id))
        annotations = self.cursor.fetchall()

        # 转换为 (xmin, ymin, xmax, ymax) 格式
        boxes = []
        for coordinates in annotations:
            xmin, ymin, xmax, ymax = map(float, coordinates[0].split(','))
            boxes.append([xmin, ymin, xmax, ymax])

        if len(boxes) == 0:
            boxes = torch.zeros((0, 4), dtype=torch.float32)
            labels = torch.zeros((0,), dtype=torch.int64)
        else:
            boxes = torch.as_tensor(boxes, dtype=torch.float32)
            labels = torch.ones((boxes.shape[0],), dtype=torch.int64)

        target = {'boxes': boxes, 'labels': labels}
        return F.to_tensor(image), target


db_path = r"E:\Tongji\Junior1\软件工程课程设计\test_database_2.db"
dataset = DatabaseDataset(db_path)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))

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
test_dataset = DatabaseDataset(db_path)
num_samples = 5  # 随机选择 5 个样本进行测试
subset_indices = random.sample(range(len(test_dataset)), num_samples)
test_subset = Subset(test_dataset, subset_indices)
test_dataloader = DataLoader(test_subset, batch_size=1, shuffle=False)

model.eval()
with torch.no_grad():
    for images, targets in test_dataloader:
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
