# PDF表格提取工具 - 生产镜像
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY extract_all_tables.py .

# 启动时工作目录为项目根，以便 backend 内 ../frontend 路径正确
ENV PORT=5000
EXPOSE 5000

# 云平台会注入 PORT；本地 docker run 时请 -e PORT=5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 --threads 4 --timeout 300 backend.wsgi:application"]
