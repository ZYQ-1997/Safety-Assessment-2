@echo off
chcp 65001 >nul
title 使用GitHub Desktop推送

echo ==========================================
echo 使用GitHub Desktop推送（最简单）
echo ==========================================
echo.
echo GitHub Desktop会自动处理认证，无需配置SSH密钥！
echo.
echo 步骤：
echo 1. 下载GitHub Desktop: https://desktop.github.com
echo 2. 安装并登录GitHub账号
echo 3. 打开GitHub Desktop
echo 4. 点击 "File" → "Add Local Repository"
echo 5. 选择项目文件夹
echo 6. 点击 "Publish repository" 或 "Push origin"
echo.
echo 正在打开GitHub Desktop下载页面...
start https://desktop.github.com
echo.
echo 安装完成后，按任意键继续...
pause

