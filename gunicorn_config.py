"""Gunicorn配置文件 - 生产环境"""
import multiprocessing
import os

# 服务器配置
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1  # 推荐的工作进程数
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5分钟超时（处理大文件需要）
keepalive = 5

# 日志配置
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程配置
daemon = False
pidfile = "gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# 性能优化
preload_app = True
max_requests = 1000
max_requests_jitter = 50

# 确保日志目录存在
os.makedirs("logs", exist_ok=True)

# WSGI应用路径（相对于项目根目录）
wsgi_app = "wsgi:application"

