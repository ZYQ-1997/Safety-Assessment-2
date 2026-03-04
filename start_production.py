# -*- coding: utf-8 -*-
"""本地模拟生产环境启动（端口、gunicorn），用于部署前自测"""
import os
import sys
import subprocess

os.environ.setdefault('FLASK_DEBUG', 'false')
port = os.environ.get('PORT', '5000')
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    try:
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', '1',
            '--threads', '4',
            '--timeout', '300',
            'app:app'
        ], check=True)
    except FileNotFoundError:
        print('请先安装 gunicorn: pip install gunicorn')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\n已停止')

if __name__ == '__main__':
    main()
