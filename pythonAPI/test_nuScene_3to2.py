from nuscenes.nuscenes import NuScenes
from nuscenes.utils.geometry_utils import view_points
from pyquaternion import Quaternion
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 初始化 nuScenes 数据集
nusc = NuScenes(version='v1.0-mini', dataroot=r'D:\datasets\nuScenes\v1.0-mini', verbose=True)

# 定义函数：将3D框投影到2D图像
def project_3d_to_2d(nusc, sample_data_token):
    # 加载样本数据
    sd_record = nusc.get('sample_data', sample_data_token)
    cs_record = nusc.get('calibrated_sensor', sd_record['calibrated_sensor_token'])
    ego_pose = nusc.get('ego_pose', sd_record['ego_pose_token'])
    
    # 获取相机参数
    cam_intrinsic = np.array(cs_record['camera_intrinsic'])
    
    # 加载图像
    img_path = nusc.get_sample_data_path(sample_data_token)
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 获取注释
    _, boxes, _ = nusc.get_sample_data(sample_data_token)
    
    for box in boxes:
        # 将box坐标变换到相机坐标系
        ego_quat = Quaternion(ego_pose['rotation'])
        cs_quat = Quaternion(cs_record['rotation'])
        
        # 应用坐标变换
        box.translate(-np.array(ego_pose['translation']))
        box.rotate(ego_quat.inverse)
        box.translate(-np.array(cs_record['translation']))
        box.rotate(cs_quat.inverse)
        
        # 投影到图像平面
        corners_3d = box.corners()
        corners_2d = view_points(corners_3d, cam_intrinsic, normalize=True)
        
        # 绘制2D边框
        x_min, y_min = np.min(corners_2d[:2, :], axis=1)
        x_max, y_max = np.max(corners_2d[:2, :], axis=1)
        x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
    
    return image

# 从数据集中选择几张图片
sample = nusc.sample[0]  # 获取第一个样本
camera_channels = ['CAM_FRONT', 'CAM_FRONT_RIGHT', 'CAM_FRONT_LEFT']
images = []

for cam in camera_channels:
    sample_data_token = sample['data'][cam]
    image_with_boxes = project_3d_to_2d(nusc, sample_data_token)
    images.append(image_with_boxes)

# 展示图片
for i, img in enumerate(images):
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.title(f"Image with 2D Bounding Boxes - {camera_channels[i]}")
    plt.axis('off')
    plt.show()
