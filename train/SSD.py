import mysql.connector
import torch
import cv2
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision.transforms import functional as F
from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
import torch.optim as optim
import matplotlib.pyplot as plt

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Step 1: 从数据库中读取数据
class DatabaseDataset(Dataset):
    def __init__(self, db_config, scene_name, is_training=True):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.scene_name = scene_name
        self.is_training = is_training

        # 获取 scene_id
        self.cursor.execute("""SELECT scene_id FROM scene_info WHERE scene_description = %s""", (self.scene_name,))
        scene_id = self.cursor.fetchone()
        if scene_id:
            self.scene_id = scene_id[0]
        else:
            raise ValueError(f"Scene '{self.scene_name}' not found in database.")

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
            sensor_data_id = self.data[idx][0]

            # 查询类别为 Car 的标注
            self.cursor.execute("""
            SELECT a2d.bbox_2d_xmin, a2d.bbox_2d_ymin, a2d.bbox_2d_xmax, a2d.bbox_2d_ymax
            FROM sensor_data sd
            JOIN sample_info si ON sd.sample_id = si.sample_id
            JOIN sample_annotation sa ON si.sample_id = sa.sample_id
            JOIN annotation_2d a2d ON sa.annotation_id = a2d.sample_annotation_id
            JOIN instance i ON sa.instance_id = i.instance_id
            WHERE sd.sensor_data_id = %s 
            AND i.category_description_id = %s
            """, (sensor_data_id, self.car_category_id))
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
        
# 数据库连接配置
remote_db_config = {
    'host': '122.51.133.37',
    'user': 'dev',
    'password': 'dev123',
    'database': 'car_perception_db'
}
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'car_perception_db'
}

dataset = DatabaseDataset(remote_db_config, scene_name='KITTI Training Data Scene', is_training=True)
dataloader = DataLoader(dataset, batch_size=4, shuffle=False, collate_fn=lambda x: tuple(zip(*x)))

# Step 2: 加载模型并训练
weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
model = ssdlite320_mobilenet_v3_large(weights=weights)
# num_classes = 2  # Background + Car
# model.head.classification_head.num_classes = num_classes
model.to(device)
model.train()

optimizer = optim.SGD(model.parameters(), lr=0.002, momentum=0.9, weight_decay=0.0005)
num_epochs = 35

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

model_save_path = 'ssdlite320_car_detector.pth'
torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")

# Step 3: 测试模型
test_dataset = DatabaseDataset(remote_db_config, scene_name='KITTI Testing Data Scene', is_training=False)
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
                if score > 0.15:  # 降低阈值以显示更多检测结果
                    xmin, ymin, xmax, ymax = box
                    cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                    cv2.putText(img, f'{score:.2f}', (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(12, 8))
            plt.imshow(img)
            plt.axis('off')
            plt.show()

dataset.close()
test_dataset.close()
