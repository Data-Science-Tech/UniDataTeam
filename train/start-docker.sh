#!/bin/bash

docker build -t my-ml-image .
docker run -v /root/datasets:/app/datasets -v /mnt:/mnt -v /root:/root -it --rm --gpus all ml-image python3 train_model.py --model_config_id 1 --scene_ids 1