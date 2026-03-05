# 部署到 Streamlit Cloud

本说明用于将 **PDF 表格提取工具** 部署到 [Streamlit Community Cloud](https://share.streamlit.io/)。

## 前置条件

- 代码已推送到 **GitHub** 公开仓库（Streamlit Cloud 仅支持 GitHub）。
- 仓库根目录包含：
  - `streamlit_app.py`（入口文件）
  - `requirements.txt`
  - `extract_all_tables.py`（与 streamlit_app 同目录）

## 部署步骤

1. **打开 Streamlit Cloud**  
   访问：<https://share.streamlit.io/>，使用 GitHub 账号登录。

2. **新建应用**  
   - 点击 **“New app”**。  
   - **Repository**：选择你的 GitHub 仓库（如 `你的用户名/Safety-Assessment-1`）。  
   - **Branch**：选择要部署的分支（一般为 `main` 或 `master`）。  
   - **Main file path**：填写 `streamlit_app.py`。  
   - **App URL**（可选）：可自定义子路径，如 `pdf-tables`。

3. **高级设置（可选）**  
   - 在 **Advanced settings** 中通常无需修改。  
   - 若需更大内存或 Python 版本，可在同一页面中设置（视 Streamlit Cloud 当前支持而定）。

4. **部署**  
   点击 **“Deploy!”**，等待构建与启动。首次部署会安装 `requirements.txt` 中的依赖，可能需要几分钟。

## 本地运行（与 Cloud 一致）

```bash
# 在项目根目录
pip install -r requirements.txt
streamlit run streamlit_app.py
```

浏览器会打开 `http://localhost:8501`。

## 注意事项

- **上传限制**：当前配置允许单文件约 500MB（可在 `.streamlit/config.toml` 中调整 `maxUploadSize`）。  
- **临时文件**：上传与生成的文件仅在当次会话的临时目录中使用，不会持久化，符合 Streamlit Cloud 无状态环境。  
- **依赖**：若部署时报错，请检查 `requirements.txt` 中版本是否与 Streamlit Cloud 支持的 Python 版本兼容（通常为 3.8–3.11）。  
- **PyMuPDF**：若在 Cloud 上安装 PyMuPDF 失败，可尝试在 `requirements.txt` 中注释或移除 `PyMuPDF`，仅使用 `pypdf`（部分复杂 PDF 的裁剪效果可能略差）。

## 项目结构（与部署相关）

```
仓库根目录/
├── streamlit_app.py      # Streamlit 入口（Cloud 主文件）
├── requirements.txt      # Python 依赖
├── extract_all_tables.py # 表格提取逻辑
├── .streamlit/
│   └── config.toml       # Streamlit 配置（主题、上传大小等）
└── STREAMLIT_CLOUD.md    # 本说明
```

部署完成后，你的应用将获得一个 `*.streamlit.app` 的公开 URL，可直接分享使用。
