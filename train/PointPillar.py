import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt

class PointCloudDataset(Dataset):
    def __init__(self, root_dir, mode='training'):
        self.point_cloud_dir = f"{root_dir}/{mode}/velodyne/"
        self.label_dir = f"{root_dir}/{mode}/label_2/" if mode == 'training' else None

    def __len__(self):
        return len([f for f in os.listdir(self.point_cloud_dir) if f.endswith('.bin')])

    def __getitem__(self, index):
        # 加载点云
        point_cloud_path = f"{self.point_cloud_dir}/{index:06d}.bin"
        points = np.fromfile(point_cloud_path, dtype=np.float32).reshape(-1, 4)  # [x, y, z, intensity]

        # 加载标签
        if self.label_dir:
            label_path = f"{self.label_dir}/{index:06d}.txt"
            labels = self._load_labels(label_path)
        else:
            labels = None

        return points, labels

    def _load_labels(self, label_path):
        labels = []
        with open(label_path, 'r') as f:
            for line in f:
                elements = line.strip().split()
                labels.append({
                    'class': elements[0],
                    'bbox_3d': [float(v) for v in elements[8:15]]  # [x, y, z, w, l, h, yaw]
                })
        return labels
    
def preprocess_points(points, grid_size=(400, 400), voxel_size=(0.2, 0.2), max_points_per_pillar=32):
    x_min, y_min = 0, 0  # 假设点云范围非负
    grid_x = ((points[:, 0] - x_min) // voxel_size[0]).astype(int)
    grid_y = ((points[:, 1] - y_min) // voxel_size[1]).astype(int)

    valid_mask = (grid_x >= 0) & (grid_x < grid_size[0]) & (grid_y >= 0) & (grid_y < grid_size[1])
    points = points[valid_mask]
    grid_x = grid_x[valid_mask]
    grid_y = grid_y[valid_mask]

    pillars = []
    indices = []
    for gx, gy in zip(grid_x, grid_y):
        mask = (grid_x == gx) & (grid_y == gy)
        pillar_points = points[mask][:max_points_per_pillar]
        if pillar_points.shape[0] < max_points_per_pillar:
            padding = np.zeros((max_points_per_pillar - pillar_points.shape[0], 4))
            pillar_points = np.vstack((pillar_points, padding))
        pillars.append(pillar_points)
        indices.append([gx, gy])

    return np.array(pillars), np.array(indices)

def create_bev_map(pillar_features, indices, grid_size=(400, 400), feature_dim=256):
    bev_map = np.zeros((grid_size[0], grid_size[1], feature_dim), dtype=np.float32)
    for feature, (gx, gy) in zip(pillar_features, indices):
        bev_map[gx, gy] = feature
    return bev_map

# PointNet for Pillar Feature Extraction
class PointNet(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(PointNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, output_dim)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return torch.max(x, dim=1)[0]  # Max pooling

# BEV Network
class BEVNet(nn.Module):
    def __init__(self, input_channels, output_channels):
        super(BEVNet, self).__init__()
        self.conv1 = nn.Conv2d(input_channels, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, output_channels, kernel_size=3, padding=1)
        self.cls_head = nn.Conv2d(output_channels, 2, kernel_size=1)  # 分类头
        self.bbox_head = nn.Conv2d(output_channels, 7, kernel_size=1)  # 边界框回归头

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = self.conv3(x)
        cls_out = self.cls_head(x)
        bbox_out = self.bbox_head(x)
        return cls_out, bbox_out
    
def compute_bbox_corners(x, y, w, l, yaw):
    corners = np.array([
        [-w / 2, -l / 2],
        [-w / 2,  l / 2],
        [ w / 2,  l / 2],
        [ w / 2, -l / 2]
    ])
    rotation_matrix = np.array([
        [np.cos(yaw), -np.sin(yaw)],
        [np.sin(yaw),  np.cos(yaw)]
    ])
    rotated_corners = np.dot(corners, rotation_matrix.T)
    global_corners = rotated_corners + np.array([x, y])
    return global_corners

from torchvision.ops import nms

def apply_nms(bbox_out, cls_out, score_threshold=0.5, iou_threshold=0.5):
    """
    后处理：非极大值抑制和边界框提取。

    Args:
        bbox_out: 模型预测的边界框回归输出，形状为 [batch_size, 7, height, width]。
        cls_out: 模型预测的分类输出，形状为 [batch_size, num_classes, height, width]。
        score_threshold: 置信度分数阈值。
        iou_threshold: NMS 的 IOU 阈值。

    Returns:
        pred_bboxes: 过滤后的边界框列表，每个边界框为 (x, y, w, l, yaw)。
        pred_scores: 每个边界框对应的置信度分数。
    """
    # 1. 计算每个网格的分类置信度和对应类别
    scores, labels = cls_out.softmax(dim=1).max(dim=1)  # 在类别维度计算 softmax，然后选择最高分

    # 2. 过滤分数低于阈值的网格
    mask = scores > score_threshold

    # 3. 过滤 bbox_out 和 scores
    bbox_out = bbox_out.permute(0, 2, 3, 1)[mask]  # 调整维度以匹配 mask，并应用 mask
    scores = scores[mask]

    if bbox_out.shape[0] == 0:  # 如果没有任何有效边界框，返回空
        return torch.empty((0, 7)), torch.empty((0,))

    # 4. 提取需要的边界框参数 [x, y, w, l, yaw]
    pred_bboxes = bbox_out[:, [0, 1, 3, 4, 6]]  # 假设这些索引对应 x, y, w, l, yaw
    pred_scores = scores

    return pred_bboxes, pred_scores




def train_one_epoch(model, dataloader, optimizer, device):
    model.train()
    total_loss = 0
    cls_loss_fn = nn.CrossEntropyLoss()
    bbox_loss_fn = nn.SmoothL1Loss()

    for points_batch, labels_batch in dataloader:
        for points, labels in zip(points_batch, labels_batch):
            # 数据预处理
            pillars, indices = preprocess_points(points.numpy())
            pillars = torch.tensor(pillars, dtype=torch.float32).to(device)
            indices = torch.tensor(indices, dtype=torch.long).to(device)

            # 提取特征并前向传播
            pillar_features = PointNet(input_dim=4, output_dim=256).to(device)(pillars)

            # 创建 BEV 映射
            bev_map = create_bev_map(pillar_features.detach().cpu().numpy(), indices.detach().cpu().numpy())
            bev_map = torch.tensor(bev_map, dtype=torch.float32).unsqueeze(0).to(device)
            bev_map = bev_map.permute(0, 3, 1, 2)  # 调整形状为 [batch_size, channels, height, width]

            cls_out, bbox_out = model(bev_map)

            # 生成目标类别（假设所有网格的类别为 1）
            batch_size, num_classes, height, width = cls_out.shape
            gt_cls = torch.ones((batch_size, height, width), dtype=torch.int64).to(device)

            # 将目标类别展平为 [batch_size * height * width]
            gt_cls = gt_cls.view(-1)

            # 调整分类输出的形状为 [batch_size * height * width, num_classes]
            cls_loss = cls_loss_fn(cls_out.permute(0, 2, 3, 1).reshape(-1, num_classes), gt_cls)

            # 假设 bbox_out 的目标为全零
            gt_bbox = torch.zeros_like(bbox_out).to(device)

            # 调整回归输出的形状
            bbox_loss = bbox_loss_fn(bbox_out.reshape(-1, 7), gt_bbox.reshape(-1, 7))
            loss = cls_loss + bbox_loss

            # 优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

    print(f"Train Loss: {total_loss / len(dataloader)}")

def test_model(model, dataloader, device, cls_loss_fn, bbox_loss_fn):
    """
    测试模型，计算损失和边界框预测。

    Args:
        model: 已训练的模型。
        dataloader: 测试数据加载器。
        device: 使用的设备（CPU 或 GPU）。
        cls_loss_fn: 分类损失函数。
        bbox_loss_fn: 边界框回归损失函数。

    Returns:
        predictions: 预测的边界框和分数。
        total_cls_loss: 平均分类损失。
        total_bbox_loss: 平均边界框损失。
    """
    model.eval()
    predictions = []
    total_cls_loss = 0.0
    total_bbox_loss = 0.0
    total_batches = 0

    with torch.no_grad():
        for points_batch, labels_batch in dataloader:
            for points, labels in zip(points_batch, labels_batch):
                points = np.array(points)  # 确保点云是 NumPy 数组
                pillars, indices = preprocess_points(points)
                pillars = torch.tensor(pillars, dtype=torch.float32).to(device)
                indices = torch.tensor(indices, dtype=torch.long).to(device)

                # 提取特征并前向传播
                pillar_features = PointNet(input_dim=4, output_dim=256).to(device)(pillars)
                bev_map = create_bev_map(pillar_features.detach().cpu().numpy(), indices.detach().cpu().numpy())
                bev_map = torch.tensor(bev_map, dtype=torch.float32).unsqueeze(0).to(device)
                bev_map = bev_map.permute(0, 3, 1, 2)

                cls_out, bbox_out = model(bev_map)

                # 打印预测输出的形状
                # print(f"cls_out shape: {cls_out.shape}, bbox_out shape: {bbox_out.shape}")

                # 后处理：提取边界框
                pred_bboxes, pred_scores = apply_nms(bbox_out, cls_out)
                predictions.append((pred_bboxes.cpu().numpy(), pred_scores.cpu().numpy()))

                # 计算分类损失和边界框回归损失
                if labels is not None:
                    # 获取真实标签
                    gt_cls = labels["cls"].to(device)
                    gt_bbox = labels["bbox"].to(device)

                    # 将 cls_out 转换为 [batch_size * height * width, num_classes]
                    cls_loss = cls_loss_fn(cls_out.permute(0, 2, 3, 1).reshape(-1, cls_out.shape[1]), gt_cls.view(-1))
                    bbox_loss = bbox_loss_fn(bbox_out.reshape(-1, bbox_out.shape[1]), gt_bbox.view(-1, bbox_out.shape[1]))

                    total_cls_loss += cls_loss.item()
                    total_bbox_loss += bbox_loss.item()
                    total_batches += 1

    # 计算平均损失
    avg_cls_loss = total_cls_loss / total_batches if total_batches > 0 else 0.0
    avg_bbox_loss = total_bbox_loss / total_batches if total_batches > 0 else 0.0

    return predictions, avg_cls_loss, avg_bbox_loss


def visualize_pointcloud_with_predictions(points, pred_bboxes):
    plt.figure(figsize=(10, 10))
    
    # 绘制点云
    plt.scatter(points[:, 0], points[:, 1], s=1, label="Point Cloud", alpha=0.5)
    
    # 绘制预测边界框
    for bbox in pred_bboxes:
        if len(bbox) >= 5:
            try:
                x, y, w, l, yaw = bbox[:5]  # 提取前五个值
                corners = compute_bbox_corners(x, y, w, l, yaw)
                plt.plot([corners[i][0] for i in [0, 1, 2, 3, 0]], 
                         [corners[i][1] for i in [0, 1, 2, 3, 0]], 
                         'r-', linewidth=1)
            except Exception as e:
                print(f"Error in computing corners for bbox {bbox}: {e}")
        else:
            print(f"Skipping invalid bbox: {bbox}")

    # 设置图例，只显示一次
    plt.plot([], [], 'r-', label="Prediction")  # 空线条用于图例显示
    plt.legend(loc="upper right")
    plt.title("Point Cloud with Predictions")
    plt.xlabel("X (meters)")
    plt.ylabel("Y (meters)")
    plt.grid(True)
    plt.axis("equal")
    plt.show()




def collate_fn(batch):
    """
    自定义 collate 函数，用于处理点云大小不一致的问题。
    Args:
        batch: 单个批次的样本列表，每个样本是 (points, labels) 的元组。
    
    Returns:
        一个批量化的列表，其中点云是列表形式，标签单独处理。
    """
    points_batch = [torch.tensor(sample[0], dtype=torch.float32) for sample in batch]
    labels_batch = [sample[1] for sample in batch]  # 如果没有标签，可能是 None
    return points_batch, labels_batch


# 入口
import torch
from torch.utils.data import DataLoader
import os

# 定义模型保存和加载路径
MODEL_DIR = "./models"
MODEL_PATH = os.path.join(MODEL_DIR, "pointpillars_model.pth")

# 初始化数据集和数据加载器
def init_data(dataset_root, batch_size=8):
    train_dataset = PointCloudDataset(dataset_root, mode='training')
    test_dataset = PointCloudDataset(dataset_root, mode='testing')

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
    return train_loader, test_loader, test_dataset

# 训练函数
def train(model, train_loader, optimizer, device, num_epochs=10):
    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        train_one_epoch(model, train_loader, optimizer, device)
    # 保存模型
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

# 测试函数
def test(model, test_loader, test_dataset, device, num_visualizations=5, visualize=False):
    print("Testing the model...")
    cls_loss_fn = nn.CrossEntropyLoss()
    bbox_loss_fn = nn.SmoothL1Loss()
    predictions, avg_cls_loss, avg_bbox_loss = test_model(model, test_loader, device, cls_loss_fn, bbox_loss_fn)
    print(f"Average Classification Loss: {avg_cls_loss:.4f}")
    print(f"Average Bounding Box Loss: {avg_bbox_loss:.4f}")
    
    if visualize:
        for i, (points, _) in enumerate(test_dataset):
            pred_bboxes, _ = predictions[i]
            visualize_pointcloud_with_predictions(points, pred_bboxes)
            if i == num_visualizations - 1:  # 控制可视化的样本数量
                break


# 加载模型
def load_model(model, device):
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        print(f"Model loaded from {MODEL_PATH}")
    else:
        print(f"No pre-trained model found at {MODEL_PATH}. Starting from scratch.")

# 主入口函数
def main(dataset_root, mode="train+test", batch_size=8, num_epochs=10, num_visualizations=5):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}\n")
    model = BEVNet(input_channels=256, output_channels=64).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # 初始化数据
    train_loader, test_loader, test_dataset = init_data(dataset_root, batch_size)

    if "train" in mode:
        print("Starting training...")
        train(model, train_loader, optimizer, device, num_epochs)

    if "test" in mode:
        print("Starting testing...")
        load_model(model, device)
        test(model, test_loader, test_dataset, device, num_visualizations)

# 执行主程序
if __name__ == "__main__":
    dataset_root = r"D:\datasets\kitti\mini_kitti"
    main(dataset_root, mode="test", batch_size=8, num_epochs=10, num_visualizations=5)
