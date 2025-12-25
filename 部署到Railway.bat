@echo off
chcp 65001 >nul
title 部署到Railway - 一键操作指南

echo ==========================================
echo PDF表格提取工具 - Railway部署指南
echo ==========================================
echo.
echo 这是最简单的部署方式，完全免费！
echo.
echo 步骤1: 准备GitHub仓库
echo ------------------------------------------
echo.
echo 如果您的代码还没有推送到GitHub，请先执行：
echo.
echo   1. 在GitHub上创建新仓库
echo   2. 运行以下命令：
echo.
echo      git init
echo      git add .
echo      git commit -m "Initial commit"
echo      git branch -M main
echo      git remote add origin https://github.com/您的用户名/仓库名.git
echo      git push -u origin main
echo.
echo 步骤2: 部署到Railway
echo ------------------------------------------
echo.
echo   1. 访问: https://railway.app
echo   2. 点击 "Login" → 选择 "Login with GitHub"
echo   3. 授权Railway访问您的GitHub账户
echo   4. 点击 "New Project"
echo   5. 选择 "Deploy from GitHub repo"
echo   6. 选择您的仓库
echo   7. Railway会自动检测Dockerfile并开始部署
echo.
echo 步骤3: 获取访问地址
echo ------------------------------------------
echo.
echo   部署完成后，Railway会提供一个URL，如：
echo   https://your-app.railway.app
echo.
echo   访问这个URL即可使用您的应用！
echo.
echo ==========================================
echo 完成！
echo ==========================================
echo.
echo 提示：
echo   - Railway提供$5/月的免费额度
echo   - 每次推送代码会自动重新部署
echo   - 支持自定义域名和HTTPS
echo.
pause

