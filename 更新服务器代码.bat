@echo off
chcp 65001 >nul
title 更新服务器代码

echo ==========================================
echo 更新服务器代码（修复502超时问题）
echo ==========================================
echo.

REM 检查Git是否安装
where git >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到Git命令行工具
    echo.
    echo 推荐使用GitHub Desktop:
    echo 1. 打开GitHub Desktop
    echo 2. 提交更改
    echo 3. 推送到GitHub
    echo 4. Railway会自动部署
    echo.
    pause
    exit /b 0
)

echo [1/4] 检查Git状态...
git status
echo.

echo [2/4] 添加所有更改的文件...
git add extract_all_tables.py backend/app.py
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)
echo ✅ 文件已添加
echo.

echo [3/4] 提交更改...
git commit -m "Fix: 优化表格列表获取，解决502超时问题

- 优化get_all_tables_info函数，添加25秒超时
- 添加快速预览模式（前100页）
- 优化表格名称提取性能
- 改进错误处理和进度报告"
if errorlevel 1 (
    echo [警告] 提交失败，可能没有更改需要提交
    echo 继续尝试推送...
) else (
    echo ✅ 更改已提交
)
echo.

echo [4/4] 推送到GitHub...
echo.
echo 提示: 如果要求输入密码，请使用GitHub的Personal Access Token
echo 生成Token: https://github.com/settings/tokens
echo.

git push origin main
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [错误] 推送失败
    echo ==========================================
    echo.
    echo 可能的原因:
    echo 1. 需要配置SSH密钥
    echo 2. 需要使用Personal Access Token
    echo 3. 远程仓库地址错误
    echo.
    echo 解决方案:
    echo 1. 使用GitHub Desktop推送（推荐）
    echo 2. 运行: 快速修复推送.bat
    echo.
) else (
    echo.
    echo ==========================================
    echo ✅ 代码已成功推送到GitHub！
    echo ==========================================
    echo.
    echo Railway会自动检测并重新部署
    echo 请等待2-5分钟，然后测试您的应用
    echo.
    echo 修复内容:
    echo - 优化表格列表获取性能
    echo - 添加25秒超时保护
    echo - 添加快速预览模式
    echo - 改进错误处理
    echo.
)

pause

