"""
【仅限本地开发】启动后端服务器（Flask 开发服务器，debug=True）。
生产部署请使用标准命令：gunicorn backend.wsgi:application（见 Procfile / Dockerfile）
"""
import os
import sys

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, 'backend')

# 切换到backend目录
os.chdir(backend_dir)

# 确保backend目录在Python路径中
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 导入并运行app
try:
    from app import app
    print("=" * 60)
    print("PDF表格提取服务启动中...")
    print("=" * 60)
    print("前端界面: http://localhost:5000")
    print("API接口: http://localhost:5000/api")
    print("=" * 60)
    print("\n按 Ctrl+C 停止服务\n")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
except KeyboardInterrupt:
    print("\n\n服务器已停止")
except Exception as e:
    print(f"\n启动失败: {e}")
    import traceback
    traceback.print_exc()
    input("\n按Enter键退出...")
    sys.exit(1)

