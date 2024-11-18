from nuscenes.nuscenes import NuScenes
from nuscenes.utils.geometry_utils import box_in_image, view_points
from PIL import Image, ImageDraw
import numpy as np
import random

# 初始化 nuScenes 数据集
nusc = NuScenes(version='v1.0-mini', dataroot='D:\\datasets\\nuScenes\\v1.0-mini', verbose=True)

def render_2d_boxes(nusc, sample_data_token):
    # 获取 sample_data 的记录
    sd_record = nusc.get('sample_data', sample_data_token)
    calib_sensor = nusc.get('calibrated_sensor', sd_record['calibrated_sensor_token'])

    # 加载图像
    img_path = nusc.get_sample_data_path(sample_data_token)
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    # 获取相机内参
    cam_intrinsic = np.array(calib_sensor['camera_intrinsic'])
    print("[DEBUG] Camera intrinsic matrix loaded.")

    # 获取 3D 框
    _, boxes, _ = nusc.get_sample_data(sample_data_token)
    print(f"[DEBUG] Total 3D boxes in scene: {len(boxes)}")

    boxes_in_image = 0  # 统计在图像范围内的框数量
    for box in boxes:
        # 筛选车辆相关的框
        if not box.name.startswith("vehicle"):
            # print(f"[INFO] Skipping non-vehicle box with name: {box.name}")
            continue

        # 打印 3D 框中心位置和深度
        box_center = box.center
        # print(f"[DEBUG] Vehicle box center in camera frame: {box_center}")

        if box_center[2] <= 0:
            print("[WARNING] Vehicle box is behind the camera. Skipping this box.")
            continue

        # 检查框是否在图像范围内
        if box_in_image(box, cam_intrinsic, img.size):
            boxes_in_image += 1
            print(f"[DEBUG] Vehicle box projected onto image successfully.")

            # 获取 3D 框在图像上的 2D 投影
            corners_3d = box.corners()
            corners_2d = view_points(corners_3d, cam_intrinsic, normalize=True)

            # 计算 2D 边界框范围
            min_x, min_y = corners_2d[:2].min(axis=1)
            max_x, max_y = corners_2d[:2].max(axis=1)
            # print(f"[DEBUG] Vehicle box 2D bounding box: {(min_x, min_y, max_x, max_y)}")

            # 绘制框在图像中的 2D 边界
            draw.rectangle([(min_x, min_y), (max_x, max_y)], outline="red", width=2)

            # 绘制框的 2D 投影点
            for corner in corners_2d.T:
                draw.ellipse((corner[0] - 3, corner[1] - 3, corner[0] + 3, corner[1] + 3), fill="blue")
        else:
            print("[INFO] Vehicle box is outside the image range.")

    print(f"[SUMMARY] Total vehicle boxes projected on image: {boxes_in_image}")
    img.show()

# 随机选择一个 sample_data_token
sample = random.choice(nusc.sample)
sample_data_token = sample['data']['CAM_FRONT']

# 调用函数绘制
render_2d_boxes(nusc, sample_data_token)
