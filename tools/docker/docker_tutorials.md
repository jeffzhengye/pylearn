# docker install

* <https://yeasy.gitbook.io/docker_practice/install/ubuntu>
* note install apt depency first.

# problem fixes

## iptables

* failed to start daemon: Error initializing network controller: error obtaining controller instance: unable to add return rule in DOCKER-ISOLATION-STAGE-1 chain:  (iptables failed: iptables --wait -A DOCKER-ISOLATION-STAGE-1 -j RETURN: iptables v1.8.7 (nf_tables):  RULE_APPEND failed (No such file or directory): rule in chain DOCKER-ISOLATION-STAGE-1
* sudo update-alternatives --config iptables
  
## Docker: Error response from daemon: OCI runtime create failed

* docker run --rm --gpus all --env NVIDIA_DISABLE_REQUIRE=1 nvidia/cuda:11.7.0-runtime-ubuntu22.04 nvidia-smi

## container search

* https://hub.docker.com/r/nvidia/cuda

## WSL启动nvidia-docker镜像：报错libnvidia-ml.so.1- file exists- unknown

## nvidia-container-cli error

* 以cpu方式进入docker，并删除所有跟nvidia相关的库so.1
* 以QAnything为例，runtime: nvidia --> runtime: runc
* sudo docker-compose up
* sudo docker exec -it  3f2293a8bdeb /bin/bash # 进入QAnything 容器，然后删除以下nvidia相关库
  * /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1
  * /usr/lib/x86_64-linux-gnu/libcudadebugger.so.1
  * /usr/lib/x86_64-linux-gnu/libcuda.so.1
  * /usr/lib/x86_64-linux-gnu/libnvidia-encode.so.1
  * mv /usr/lib/x86_64-linux-gnu/libnvidia-allocator.so.1 /usr/lib/x86_64-linux-gnu/libnvcuvid.so.1 bakup
  * find /usr/lib/x86_64-linux-gnu/ -name *nv*
* sudo docker commit 3f2293a8bdeb freeren/qanything:v2.0.7 # 重新打镜像，并把QAnything runtime:nvidia, 镜像名改为freeren/qanything:v2.0.7

# start docker

* sudo service docker start
* sudo dockerd

# stop a running container

* docker stop containerID or containerName

# config your docker user

* https://docs.docker.com/engine/install/linux-postinstall

## add user to docker group

* sudo usermod -aG docker $USER
* newgrp docker
* sudo chmod a+rw /var/run/docker.sock
* sudo systemctl restart docker


# Upgraded docker-compose the official docker/non-Debian-way

$ sudo curl -L "<https://github.com/docker/compose/releases/download/1.27.4/docker-compose>-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ which docker-compose
/usr/local/bin/docker-compose
$ docker-compose -v
docker-compose version 1.27.4, build 40524192

# list all dockers

* sudo docker ps -a

# enter a specified docker

* sudo docker exec -it  89ce35817c64 /bin/bash  $ change the docker id.
* 没有bash 改为 sh

# df

* docker system df

# commit - 新建一个镜像

* sudo docker commit 3f2293a8bdeb[base container id] freeren/qanything:v2.0.7[name and tag]

# create a new container

* sudo docker run -it cdaudt/ubuntu-byobu
* docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag

# exec

* 是进入已经存在的容器，run是创建新容器

# port

* docker port 89ce35817c64 # 显示端口映射

# docker mysql note: have to setup password for root, 也可以在网页版后台环境变量中设置

* docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag

# To start an existing container which is stopped

* docker start <container-name/ID>

# To start an existing container and attach to it in one command

* docker start -ai <container-name/ID>

# 国内加速

https://registry.hub.docker.com

* sudo vi /etc/docker/daemon.json
{
 "registry-mirrors": ["https://registry.docker-cn.com",
                      "http://hub-mirror.c.163.com" ,
                      "https://kfwkfulq.mirror.aliyuncs.com"]
}

* 国内不能用时
  * https://gist.github.com/y0ngb1n/7e8f16af3242c7815e7ca2f0833d3ea6

# 运行镜像，并映射目录

## 运行PaddlePaddle语音识别镜像，这里设置与主机共同拥有IP和端口号

sudo nvidia-docker run -it --net=host -v $(pwd)/DeepSpeech:/DeepSpeech registry.baidubce.com/paddlepaddle/paddle:2.1.2-gpu-cuda10.2-cudnn7 /bin/bash

# persisting your data

* Volumes are the preferred way to persist data in Docker.
  * [Volumes](https://docs.docker.com/storage/volumes/)
  * 存储位置：sudo ls /var/lib/docker/volumes/
  * 如何备份： 

# runtime

## show runtime

* docker info|grep -i runtime

## install nvidia runtime

* sudo apt-get install nvidia-container-runtime
* sudo vim /etc/docker/daemon.json
```
{
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
```

* sudo pkill -SIGHUP dockerd

# docker file: Dockerfile

## copy fold

* COPY testdir ./testdir


# docker 监控

## ctop image

* sudo docker run --name ctop --rm -ti -v /var/run/docker.sock:/var/run/docker.sock:ro quay.io/vektorlab/ctop:latest

# docker-compose

## tutorials

* [official](https://docs.docker.com/compose/)
* [中文](https://yeasy.gitbook.io/docker_practice/compose/compose_file)

## 启动

* docker compose up -d
  * the -d flag tells Docker Compose to run in detached mode.

## build

* 指定Dockerfile的路径

## 重新构建 rebuilt

* docker-compose up --build

## volumes

* 作用：管理容器之间的数据共享；数据卷可以用来持久化存储容器中的数据，即使容器被删除了，数据卷中的数据仍然存在。
  * 创建的数据卷可以理解为在宿主机上的一个特殊存储区域，但它不一定是传统意义上的单一目录。从功能上看，它表现得像一个独立的存储位置，与宿主机的文件系统有一定的隔离性。Docker 会管理这个存储区域，使得容器可以方便地挂载和使用它来存储数据。
* 备份： 找到数据卷在宿主机上的实际存储位置。这通常取决于 Docker 的存储驱动和配置，对于一些存储驱动，数据卷可能以目录的形式存在于宿主机文件系统中。例如，在使用某些版本的本地存储驱动时，可以在 /var/lib/docker/volumes/ 目录下找到数据卷对应的目录。使用传统的文件复制工具（如 cp、rsync 等）将该目录复制到备份位置。
  * 但需要注意的是，不同的存储驱动和 Docker 版本可能会使数据卷在宿主机上的存储方式有所不同，不一定总是能以这种方式直接查看
* volumes是存储在宿主机上的目录，可以被容器挂载；数据持久化，防止容器销毁数据丢失。
* ./app:/app ：将当前目录下的app目录挂载到容器的/app目录下
* ./app:/app:ro ：ro：只读


## working_dir

* 

## watch

* [例子](https://github.com/docker/multi-container-app/blob/main/compose.yaml)
  * When developing with Docker, you may need to automatically update and preview your running services as you edit and save your code. You can use Docker Compose Watch for this.

## docker compose kill

* docker-compose kill -s SIGINT

## ports

* "8080:80" : 将宿主机的8080端口映射到容器的80端口

## 查看log

* docker-compose logs -f service_name

## problems shotting

### docker Could not set file permission for ca.pem

* ![Alt text](image.png)

