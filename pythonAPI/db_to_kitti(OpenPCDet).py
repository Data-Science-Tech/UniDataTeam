import os
import shutil
import numpy as np
import mysql.connector
from pathlib import Path
from typing import List, Dict, Tuple
import logging


class MySQLToKITTIConverter:
    def __init__(self, db_config: Dict, output_base_path: str):
        """
        初始化转换器
        :param db_config: MySQL数据库配置
        :param output_base_path: 输出基础路径
        """
        self.db_config = db_config
        self.output_base_path = Path(output_base_path)
        self.kitti_path = self.output_base_path / 'kitti'
        self.conn = None
        self.cursor = None
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def connect_db(self):
        """建立数据库连接"""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor(dictionary=True)
            self.logger.info("Successfully connected to database")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise

    def create_directory_structure(self):
        """创建KITTI数据集目录结构"""
        dirs = [
            'ImageSets',
            'training/calib',
            'training/velodyne',
            'training/label_2',
            'training/image_2',
            'testing/calib',
            'testing/velodyne',
            'testing/image_2'
        ]

        for dir_path in dirs:
            full_path = self.kitti_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {full_path}")

    def get_sample_splits(self):
        """获取训练集、验证集和测试集的样本ID"""
        query = """  
        SELECT si.sample_id, sci.scene_id  
        FROM sample_info si  
        JOIN scene_info sci ON si.scene_id = sci.scene_id  
        ORDER BY si.sample_id  
        """
        self.cursor.execute(query)
        samples = self.cursor.fetchall()

        if not samples:
            self.logger.error("No samples found in database!")
            raise ValueError("No samples found in database")

            # 首先分离训练数据和测试数据
        train_val_ids = []
        test_ids = []

        for sample in samples:
            if sample['scene_id'] == 1:
                train_val_ids.append(sample['sample_id'])
            elif sample['scene_id'] == 2:
                test_ids.append(sample['sample_id'])

                # 从训练数据中划分出验证集（10%）
        num_val = int(len(train_val_ids))  # 暂时全部作为验证集
        train_ids = train_val_ids[:num_val]
        val_ids = train_val_ids[:num_val]

        self.logger.info(f"Split samples: train({len(train_ids)}), "
                         f"val({len(val_ids)}), test({len(test_ids)})")

        return train_ids, val_ids, test_ids

    def write_split_files(self, train_ids, val_ids, test_ids):
        """写入数据集划分文件"""
        # 创建ImageSets目录
        imageset_dir = self.kitti_path / 'ImageSets'
        imageset_dir.mkdir(exist_ok=True)

        # 确保所有ID都被格式化为6位数的字符串
        def format_ids(ids):
            return [f'{idx:06d}' for idx in sorted(ids)]

        # 写入训练集文件
        train_ids_formatted = format_ids(train_ids)
        with open(imageset_dir / 'train.txt', 'w') as f:
            f.write('\n'.join(train_ids_formatted))
            if train_ids_formatted:  # 确保最后有换行符
                f.write('\n')

        # 写入验证集文件 (即使为空也需要创建文件)
        val_ids_formatted = format_ids(val_ids) if val_ids else []
        with open(imageset_dir / 'val.txt', 'w') as f:
            f.write('\n'.join(val_ids_formatted))
            if val_ids_formatted:  # 确保最后有换行符
                f.write('\n')

        # 写入测试集文件
        test_ids_formatted = format_ids(test_ids)
        with open(imageset_dir / 'test.txt', 'w') as f:
            f.write('\n'.join(test_ids_formatted))
            if test_ids_formatted:  # 确保最后有换行符
                f.write('\n')

        self.logger.info(f"Written split files: train({len(train_ids_formatted)}), "
                         f"val({len(val_ids_formatted)}), test({len(test_ids_formatted)})")

    def convert_calibration(self, sample_id: int, is_training: bool):
        """转换标定数据"""
        query = """
        SELECT sc.*, s.sensor_type 
        FROM sensor_calibration sc
        JOIN sensor_data sd ON sd.sensor_calibration_id = sc.sensor_calibration_id
        JOIN sensor s ON sc.sensor_id = s.sensor_id
        WHERE sd.sample_id = %s
        """
        self.cursor.execute(query, (sample_id,))
        calibs = self.cursor.fetchall()

        if not calibs:
            self.logger.warning(f"No calibration data found for sample {sample_id}")
            return

        # 生成KITTI格式的标定文件
        calib_dir = 'training' if is_training else 'testing'
        calib_path = self.kitti_path / calib_dir / 'calib' / f'{sample_id:06d}.txt'

        # 默认标定矩阵（来自KITTI数据集的典型值）
        default_P2 = np.array([[721.5377, 0., 609.5593, 44.85728],
                               [0., 721.5377, 172.854, 0.2163791],
                               [0., 0., 1., 0.002745884]])

        default_Tr = np.array([[7.533745e-03, -9.999714e-01, -6.166020e-04, -4.069766e-03],
                               [1.480249e-02, 7.280733e-04, -9.998902e-01, -7.631618e-02],
                               [9.998621e-01, 7.523790e-03, 1.480755e-02, -2.717806e-01]])

        # R0_rect是3x3的单位矩阵
        R0_rect = np.eye(3)

        # 准备数据
        P2 = default_P2.copy()
        Tr = default_Tr.copy()
        camera_found = False
        lidar_found = False

        # 处理标定数据
        for calib in calibs:
            if calib['sensor_type'].lower() == 'camera':
                camera_found = True
                try:
                    P2 = np.zeros((3, 4))
                    P2[0, 0] = calib['focal_length_x'] or default_P2[0, 0]
                    P2[1, 1] = calib['focal_length_y'] or default_P2[1, 1]
                    P2[0, 2] = calib['principal_point_x'] or default_P2[0, 2]
                    P2[1, 2] = calib['principal_point_y'] or default_P2[1, 2]
                    P2[0, 3] = calib['translation_x'] or default_P2[0, 3]
                    P2[1, 3] = calib['translation_y'] or default_P2[1, 3]
                    P2[2, 3] = calib['translation_z'] or default_P2[2, 3]
                    P2[2, 2] = 1.0
                except (TypeError, ValueError):
                    P2 = default_P2

            elif calib['sensor_type'].lower() == 'lidar':
                lidar_found = True
                try:
                    if all(calib[k] is not None for k in ['rotation_roll', 'rotation_pitch', 'rotation_yaw',
                                                          'translation_x', 'translation_y', 'translation_z']):
                        R = self._euler_to_rotation_matrix(
                            float(calib['rotation_roll']),
                            float(calib['rotation_pitch']),
                            float(calib['rotation_yaw'])
                        )
                        T = np.array([
                            float(calib['translation_x']),
                            float(calib['translation_y']),
                            float(calib['translation_z'])
                        ])
                        Tr = np.hstack((R, T.reshape(3, 1)))
                except (TypeError, ValueError):
                    Tr = default_Tr

        # 按KITTI格式的固定顺序写入文件
        with open(calib_path, 'w') as f:
            # 1. 写入P0（与P2相同）
            f.write(f"P0: {' '.join(map(str, P2.flatten()))}\n")

            # 2. 写入P1（与P2相同）
            f.write(f"P1: {' '.join(map(str, P2.flatten()))}\n")

            # 3. 写入P2
            f.write(f"P2: {' '.join(map(str, P2.flatten()))}\n")

            # 4. 写入P3（与P2相同）
            f.write(f"P3: {' '.join(map(str, P2.flatten()))}\n")

            # 5. 写入R0_rect（3x3矩阵）
            f.write(f"R0_rect: {' '.join(map(str, R0_rect.flatten()[:9]))}\n")

            # 6. 写入Tr_velo_to_cam
            f.write(f"Tr_velo_to_cam: {' '.join(map(str, Tr.flatten()))}\n")

    def _euler_to_rotation_matrix(self, roll, pitch, yaw):
        """欧拉角转旋转矩阵"""
        # 确保输入是浮点数
        roll = float(roll)
        pitch = float(pitch)
        yaw = float(yaw)

        R_x = np.array([[1, 0, 0],
                        [0, np.cos(roll), -np.sin(roll)],
                        [0, np.sin(roll), np.cos(roll)]])

        R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                        [0, 1, 0],
                        [-np.sin(pitch), 0, np.cos(pitch)]])

        R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                        [np.sin(yaw), np.cos(yaw), 0],
                        [0, 0, 1]])

        return R_z @ R_y @ R_x

    def convert_labels(self, sample_id: int):
        """转换标注数据到KITTI格式"""
        query = """  
        SELECT sa.*, cd.category_subcategory_name  
        FROM sample_annotation sa  
        JOIN instance i ON sa.instance_id = i.instance_id  
        JOIN category_description cd ON i.category_description_id = cd.category_description_id  
        WHERE sa.sample_id = %s  
        """
        self.cursor.execute(query, (sample_id,))
        annotations = self.cursor.fetchall()

        label_path = self.kitti_path / 'training' / 'label_2' / f'{sample_id:06d}.txt'

        # KITTI默认值
        default_values = {
            'truncated': 0,
            'occluded': 0,
            'alpha': -10,
            'bbox_2d_xmin': 0,
            'bbox_2d_ymin': 0,
            'bbox_2d_xmax': 50,
            'bbox_2d_ymax': 50,
            'bbox_3d_height_z': 1.5,
            'bbox_3d_width_y': 1.5,
            'bbox_3d_length_x': 3.5,
            'bbox_center_3d_x': 0,
            'bbox_center_3d_y': 0,
            'bbox_center_3d_z': 0,
            'rotation_yaw': 0
        }

        with open(label_path, 'w') as f:
            for ann in annotations:
                try:
                    # 确保category_subcategory_name存在，如果不存在使用默认值'DontCare'
                    obj_type = ann.get('category_subcategory_name', 'DontCare')

                    # 使用get方法获取值，如果为None则使用默认值
                    bbox_2d_xmin = ann.get('bbox_2d_xmin', default_values['bbox_2d_xmin'])
                    bbox_2d_ymin = ann.get('bbox_2d_ymin', default_values['bbox_2d_ymin'])
                    bbox_2d_xmax = ann.get('bbox_2d_xmax', default_values['bbox_2d_xmax'])
                    bbox_2d_ymax = ann.get('bbox_2d_ymax', default_values['bbox_2d_ymax'])

                    height = ann.get('bbox_3d_height_z', default_values['bbox_3d_height_z'])
                    width = ann.get('bbox_3d_width_y', default_values['bbox_3d_width_y'])
                    length = ann.get('bbox_3d_length_x', default_values['bbox_3d_length_x'])

                    x = ann.get('bbox_center_3d_x', default_values['bbox_center_3d_x'])
                    y = ann.get('bbox_center_3d_y', default_values['bbox_center_3d_y'])
                    z = ann.get('bbox_center_3d_z', default_values['bbox_center_3d_z'])

                    rotation_y = ann.get('rotation_yaw', default_values['rotation_yaw'])

                    # 确保所有值都是数值类型
                    values = [
                        bbox_2d_xmin, bbox_2d_ymin, bbox_2d_xmax, bbox_2d_ymax,
                        height, width, length, x, y, z, rotation_y
                    ]

                    # 将None转换为默认值
                    values = [default_values[k] if v is None else float(v) for k, v in zip(
                        ['bbox_2d_xmin', 'bbox_2d_ymin', 'bbox_2d_xmax', 'bbox_2d_ymax',
                         'bbox_3d_height_z', 'bbox_3d_width_y', 'bbox_3d_length_x',
                         'bbox_center_3d_x', 'bbox_center_3d_y', 'bbox_center_3d_z',
                         'rotation_yaw'],
                        values
                    )]

                    # KITTI格式：type truncated occluded alpha bbox2D_left bbox2D_top bbox2D_right bbox2D_bottom height width length x y z rotation_y
                    kitti_line = (f"{obj_type} "
                                  f"{default_values['truncated']:.2f} "
                                  f"{default_values['occluded']} "
                                  f"{default_values['alpha']:.2f} "
                                  f"{values[0]:.2f} {values[1]:.2f} "
                                  f"{values[2]:.2f} {values[3]:.2f} "
                                  f"{values[4]:.2f} {values[5]:.2f} "
                                  f"{values[6]:.2f} "
                                  f"{values[7]:.2f} {values[8]:.2f} "
                                  f"{values[9]:.2f} {values[10]:.2f}\n")

                    f.write(kitti_line)

                except Exception as e:
                    self.logger.warning(f"Error processing annotation for sample {sample_id}: {e}")
                    # 如果处理单个标注出错，写入一个DontCare对象
                    f.write(f"DontCare 0 0 -10 0 0 50 50 1.5 1.5 3.5 0 0 0 0\n")
                    continue

        self.logger.info(f"Converted labels for sample {sample_id}")

    def copy_sensor_data(self, sample_id: int, is_training: bool):
        """复制传感器数据（图像和点云）"""
        query = """
        SELECT sd.*, s.sensor_type
        FROM sensor_data sd
        JOIN sensor_calibration sc ON sd.sensor_calibration_id = sc.sensor_calibration_id
        JOIN sensor s ON sc.sensor_id = s.sensor_id
        WHERE sd.sample_id = %s
        """
        self.cursor.execute(query, (sample_id,))
        sensor_data = self.cursor.fetchall()

        split_dir = 'training' if is_training else 'testing'

        for data in sensor_data:
            source_path = data['file_path']

            if data['sensor_type'] == 'camera':
                target_dir = self.kitti_path / split_dir / 'image_2'
                target_path = target_dir / f'{sample_id:06d}.png'
            elif data['sensor_type'] == 'lidar':
                target_dir = self.kitti_path / split_dir / 'velodyne'
                target_path = target_dir / f'{sample_id:06d}.bin'

            try:
                shutil.copy2(source_path, target_path)
            except Exception as e:
                self.logger.error(f"Failed to copy {source_path} to {target_path}: {e}")

    def convert(self):
        """执行完整的转换过程"""
        try:
            self.connect_db()
            self.create_directory_structure()

            # 获取数据集划分
            train_ids, val_ids, test_ids = self.get_sample_splits()
            self.write_split_files(train_ids, val_ids, test_ids)

            # 处理训练集
            for sample_id in train_ids + val_ids:
                self.convert_calibration(sample_id, True)
                self.convert_labels(sample_id)
                self.copy_sensor_data(sample_id, True)
                self.logger.info(f"Processed training sample: {sample_id}")

            # 处理测试集
            for sample_id in test_ids:
                self.convert_calibration(sample_id, False)
                self.copy_sensor_data(sample_id, False)
                self.logger.info(f"Processed testing sample: {sample_id}")

        except Exception as e:
            self.logger.error(f"Conversion failed: {e}")
            raise
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            self.logger.info("Conversion completed")


if __name__ == "__main__":
    # 数据库配置
    db_config = {
        'host': '122.51.133.37',
        'user': 'dev',
        'password': 'dev123',
        'database': 'car_perception_db'
    }

    # 输出路径配置
    output_path = '../../'

    # 创建转换器实例并执行转换
    converter = MySQLToKITTIConverter(db_config, output_path)
    converter.convert()