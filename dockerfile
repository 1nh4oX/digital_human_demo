######### 废案 ##########
# 基础镜像（带 Node + Python）
FROM node:18-bullseye

# 安装 Python
RUN apt update && apt install -y python3 python3-pip python3-venv

# 设置工作目录
WORKDIR /app

# 拷贝所有代码
COPY . .

# 安装 Python 依赖
RUN pip3 install --upgrade pip
RUN pip3 install -r Brain/requirements.txt

# 安装前端依赖
WORKDIR /app/Front/digital-human-front
RUN npm install

# 设置默认工作目录为根
WORKDIR /app

# 启动脚本（包含 Flask + Vite）
CMD ["sh", "start.sh"]