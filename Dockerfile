# PDF表格提取工具 - 生产镜像
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY extract_all_tables.py .

# Hugging Face Spaces 默认端口 7860；本地可 -e PORT=5000
ENV PORT=7860
EXPOSE 7860

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-7860} --workers 1 --threads 4 --timeout 300 backend.wsgi:application"]
