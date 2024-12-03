# 使用基础镜像（带 CUDA 支持的 PyTorch 镜像）
FROM nvidia/cuda:12.6.2-cudnn-devel-ubuntu22.04

# 安装 Python 3.10 和必要系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3-pip python3.10-dev libmysqlclient-dev git \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 设置 Python 3.10 为默认版本
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# 安装 Python 包
RUN pip install --no-cache-dir \
    torch torchvision mysql-connector-python \
    numpy opencv-python opencv-contrib-python matplotlib

# 设置工作目录
WORKDIR /app

# 复制当前目录下的代码到容器
COPY . /app

# 默认启动命令
CMD ["python", "train_model.py", "--model_config_id", "1", "--scene_ids", "3"]
