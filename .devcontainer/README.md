# Dev Container 说明

- **端口**：Flask 监听 `0.0.0.0:5000`，Codespaces 会自动转发 5000。
- **依赖**：首次创建容器时会执行 `pip install -r requirements.txt`。
- **自动启动**：容器启动后会后台运行 `start_server.py`；若未运行，在终端执行 `python start_server.py`。
- **日志**：自动启动时输出在 `/tmp/flask-server.log`。
