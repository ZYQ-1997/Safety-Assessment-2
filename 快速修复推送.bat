@echo off
chcp 65001 >nul
title 修复Git推送问题

echo ==========================================
echo 修复Git推送权限问题
echo ==========================================
echo.
echo 问题：Permission denied (publickey)
echo.
echo 解决方案：改用HTTPS方式
echo ==========================================
echo.

echo 请提供以下信息：
echo.
set /p github_user="GitHub用户名: "
set /p repo_name="仓库名称: "

echo.
echo 正在修改远程仓库地址...
git remote set-url origin https://github.com/%github_user%/%repo_name%.git

echo.
echo ✅ 已修改为HTTPS方式
echo.
echo 现在可以推送了：
echo   git push origin main
echo.
echo 提示：如果要求输入密码，请使用GitHub的Personal Access Token
echo 生成Token: https://github.com/settings/tokens
echo.
pause

