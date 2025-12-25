# 使用Python 3.10作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装Gunicorn（生产环境WSGI服务器）
RUN pip install --no-cache-dir gunicorn

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p backend/uploads backend/outputs logs

# 设置环境变量
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:application"]

