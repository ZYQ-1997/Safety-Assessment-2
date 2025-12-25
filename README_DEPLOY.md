# 🚀 快速部署指南（无云服务器版）

## 您没有云服务器？没问题！

我们使用**免费的云平台**来部署，完全自动化，无需手动配置！

## ⚡ 最快方式（3步完成）

### 1. 准备GitHub仓库

**最简单的方法 - 使用GitHub Desktop：**

1. 下载：https://desktop.github.com
2. 安装并登录GitHub账号
3. 打开GitHub Desktop
4. 点击 "File" → "Add Local Repository"
5. 选择项目文件夹（Safety Assessment）
6. 点击 "Publish repository"
7. 完成！

**或者使用网页：**

1. 访问：https://github.com/new
2. 创建新仓库（名称：pdf-table-extractor）
3. 点击 "uploading an existing file"
4. 上传项目文件（拖拽整个文件夹）
5. 点击 "Commit changes"

### 2. 部署到Railway

1. 访问：https://railway.app
2. 点击 "Login" → 选择 "Login with GitHub"
3. 授权Railway访问GitHub
4. 点击 "New Project"
5. 选择 "Deploy from GitHub repo"
6. 选择您的仓库
7. **完成！** Railway会自动部署

### 3. 获取访问地址

部署完成后（通常2-5分钟）：
- Railway会自动分配一个URL，如：`https://your-app.railway.app`
- 访问这个URL即可使用您的应用！

## 🎁 免费额度

Railway提供：
- **$5/月免费额度**（足够小型应用使用）
- 自动HTTPS
- 自动域名
- 支持自定义域名
- 自动重新部署（每次推送代码）

## 📱 一键操作

运行以下文件获取详细指导：
```bash
开始部署.bat
```

## 🔄 自动更新

每次您推送代码到GitHub，Railway会自动重新部署！

## ❓ 常见问题

**Q: 需要付费吗？**
A: 不需要！Railway提供$5/月免费额度，足够使用。

**Q: 部署需要多长时间？**
A: 通常2-5分钟。

**Q: 如何更新应用？**
A: 推送代码到GitHub，Railway会自动更新。

**Q: 可以自定义域名吗？**
A: 可以！在Railway项目设置中添加自定义域名。

## 🆘 需要帮助？

1. 查看 `最简单部署指南.md` 获取详细步骤
2. 运行 `开始部署.bat` 获取交互式指导
3. Railway文档：https://docs.railway.app

