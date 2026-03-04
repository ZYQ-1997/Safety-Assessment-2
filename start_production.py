# -*- coding: utf-8 -*-
"""
生产环境启动入口（标准模式）。
从项目根目录运行，使用 gunicorn + backend.wsgi:application，端口与调试由环境变量控制。
"""
import os
import sys
import subprocess

project_root = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("FLASK_DEBUG", "false")
port = os.environ.get("PORT", "5000")
# 确保从项目根加载 backend 包（避免 No module named 'backend.wsgi'）
os.environ["PYTHONPATH"] = project_root

def main():
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "gunicorn",
                "--bind", f"0.0.0.0:{port}",
                "--workers", "1",
                "--threads", "4",
                "--timeout", "300",
                "backend.wsgi:application",
            ],
            cwd=project_root,
            check=True,
        )
    except FileNotFoundError:
        print("请先安装 gunicorn: pip install gunicorn")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已停止")

if __name__ == "__main__":
    main()
