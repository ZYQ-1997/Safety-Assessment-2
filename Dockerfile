# PDF表格提取工具 - 生产镜像
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY extract_all_tables.py .

ENV PYTHONPATH=/app
ENV PORT=7860
EXPOSE 7860

# 标准生产入口：直接调用 gunicorn（PORT 由环境变量注入，默认 7860）
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-7860} --workers 1 --threads 4 --timeout 300 backend.wsgi:application"]
