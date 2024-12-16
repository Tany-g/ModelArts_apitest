# 指定基础镜像为 Ubuntu 20.04
ARG all_proxy=172.17.128.1:7890

FROM ubuntu:20.04


ENV all_proxy=172.17.128.1:7890
# 换源或者使用代理

# 安装 Python 3 和 pip3
RUN apt-get update && apt-get install -y python3 python3-pip


# 安装 requirements.txt 文件中列出的 Python 依赖
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# 将当前目录下的所需文件复制到容器的 /workspace 目录中
COPY model /workspace/model
COPY service.py /workspace
COPY label.txt /workspace
WORKDIR /workspace

ENV all_proxy=
EXPOSE 8080
# 容器启动后执行的命令，运行 service.py 脚本
CMD ["/bin/python3", "service.py"]