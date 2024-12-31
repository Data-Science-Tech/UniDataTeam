# UniDataTeam

## 如何部署到服务器上

- 先在本地运行：

  ```bash
  docker-compose -f docker-compose.deploy.yml build
  ```

- 在本地把镜像保存为tar文件：

  ```bash
  docker save -o frontend_image_deploy.tar uni-datateam_frontend_deploy:latest
  docker save -o backend_image_deploy.tar uni-datateam_backend_deploy:latest
  ```

- 在本地终端把文件放到服务器上

  ```bash
  scp frontend_image_deploy.tar backend_image_deploy.tar docker-compose.server.yml ubuntu@122.51.133.37:/home/ubuntu/uniDataService
  ```

- 在服务器上加载镜像

  ```bash
  sudo docker load -i frontend_image_deploy.tar
  sudo docker load -i backend_image_deploy.tar
  ```

- 在服务器上启动服务

  ```bash
  sudo docker-compose -f docker-compose.server.yml up -d
  ```

- 在服务器上关闭服务

  ```bash
  sudo docker-compose -f docker-compose.server.yml down
  ```

  

### 服务器上的镜像删除

```
sudo docker rm unidataservice-frontend_deploy-1
sudo docker rm unidataservice-backend_deploy-1
sudo docker rmi uni-datateam_frontend_deploy:latest
sudo docker rmi uni-datateam_backend_deploy:latest
```

