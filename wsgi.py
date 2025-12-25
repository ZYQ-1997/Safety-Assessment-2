"""
WSGI入口文件 - 用于生产环境部署
"""
import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = Path(__file__).parent.absolute()
backend_dir = project_root / 'backend'

# 添加项目根目录和backend目录到Python路径
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# 切换到backend目录（确保相对路径正确）
os.chdir(str(backend_dir))

# 导入Flask应用
from app import app

# 生产环境配置
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# 这是WSGI应用对象，Gunicorn会使用它
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)

