#!/bin/bash

# 数据集下载到服务器上
scp -P 41661 -r /mnt/d/datasets root@36.213.48.208:/root

scp -P 41661 fasterrcnn_resnet50_fpn_coco-258fb6c6.pth root@36.213.48.208:/root/.cache/torch/hub/checkpoints/

scp -P 41661 train_model.py root@36.213.48.208:/root/docker

docker build -t my-ml-image .
docker run -v /mnt/d/datasets:/app/datasets -v /mnt:/mnt -v /root:/root -it --rm --gpus all ml-image python3 train_model.py --model_config_id 1 --scene_ids 1 --training_result_id 159