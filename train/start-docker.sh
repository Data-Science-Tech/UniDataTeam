#!/bin/bash

docker build -t my-ml-image .
docker run -v /mnt/d/datasets:/app/datasets -it --rm --gpus all --name my-ml-container my-ml-image