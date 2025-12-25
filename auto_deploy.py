#!/usr/bin/env python3
"""
自动化部署脚本
支持多种云平台自动部署
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """检查必要的依赖"""
    required = ['docker', 'docker-compose']
    missing = []
    
    for cmd in required:
        try:
            subprocess.run([cmd, '--version'], 
                         capture_output=True, 
                         check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(cmd)
    
    if missing:
        print(f"❌ 缺少必要的工具: {', '.join(missing)}")
        print("请先安装这些工具")
        return False
    return True

def deploy_local():
    """本地部署"""
    print("🚀 开始本地部署...")
    
    try:
        # 停止现有容器
        print("📦 停止现有容器...")
        subprocess.run(['docker-compose', 'down'], check=False)
        
        # 构建镜像
        print("🔨 构建Docker镜像...")
        subprocess.run(['docker-compose', 'build', '--no-cache'], check=True)
        
        # 启动服务
        print("▶️  启动服务...")
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        
        # 等待服务启动
        import time
        print("⏳ 等待服务启动...")
        time.sleep(5)
        
        # 检查服务状态
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, 
                              text=True)
        print(result.stdout)
        
        print("✅ 部署完成！")
        print("🌐 访问地址: http://localhost:5000")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署失败: {e}")
        return False

def deploy_to_server(host, user, key_path=None):
    """部署到远程服务器"""
    print(f"🚀 开始部署到服务器 {user}@{host}...")
    
    # 构建部署命令
    deploy_script = f"""
    set -e
    cd /opt/pdf-extractor || mkdir -p /opt/pdf-extractor && cd /opt/pdf-extractor
    docker-compose down 2>/dev/null || true
    docker-compose build --no-cache
    docker-compose up -d
    docker image prune -f
    echo "✅ 部署完成！"
    """
    
    # 复制文件到服务器
    print("📤 上传文件到服务器...")
    project_dir = Path(__file__).parent
    
    # 使用rsync或scp上传文件
    rsync_cmd = [
        'rsync', '-avz', '--exclude', '.git',
        '--exclude', '__pycache__',
        '--exclude', '*.pyc',
        '--exclude', 'backend/uploads/*',
        '--exclude', 'backend/outputs/*',
        f'{project_dir}/',
        f'{user}@{host}:/opt/pdf-extractor/'
    ]
    
    if key_path:
        rsync_cmd.insert(1, '-e')
        rsync_cmd.insert(2, f'ssh -i {key_path}')
    
    try:
        subprocess.run(rsync_cmd, check=True)
        print("✅ 文件上传完成")
    except subprocess.CalledProcessError:
        print("⚠️  rsync不可用，尝试使用scp...")
        # 使用scp作为备选
        scp_cmd = ['scp', '-r', str(project_dir), f'{user}@{host}:/opt/']
        if key_path:
            scp_cmd.insert(1, '-i')
            scp_cmd.insert(2, key_path)
        subprocess.run(scp_cmd, check=True)
    
    # 执行部署命令
    print("🔧 在服务器上执行部署...")
    ssh_cmd = ['ssh', f'{user}@{host}']
    if key_path:
        ssh_cmd.insert(1, '-i')
        ssh_cmd.insert(2, key_path)
    ssh_cmd.append('bash -s')
    
    try:
        process = subprocess.Popen(ssh_cmd, 
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
        stdout, stderr = process.communicate(input=deploy_script)
        
        if process.returncode == 0:
            print(stdout)
            print("✅ 部署完成！")
            return True
        else:
            print(f"❌ 部署失败: {stderr}")
            return False
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False

def deploy_railway():
    """部署到Railway"""
    print("🚀 准备部署到Railway...")
    print("📝 请确保已安装Railway CLI: npm i -g @railway/cli")
    print("📝 请先登录: railway login")
    
    try:
        subprocess.run(['railway', 'up'], check=True)
        print("✅ Railway部署完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Railway部署失败: {e}")
        print("请确保已安装并登录Railway CLI")
        return False

def deploy_render():
    """部署到Render"""
    print("🚀 Render部署需要手动配置:")
    print("1. 访问 https://render.com")
    print("2. 创建新的Web Service")
    print("3. 连接GitHub仓库")
    print("4. 使用Docker部署")
    print("5. 设置环境变量（如需要）")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("PDF表格提取工具 - 自动化部署")
    print("=" * 60)
    print()
    
    if not check_dependencies():
        sys.exit(1)
    
    # 检查部署方式
    if len(sys.argv) > 1:
        deploy_type = sys.argv[1]
    else:
        print("请选择部署方式:")
        print("1. 本地部署 (localhost)")
        print("2. 远程服务器部署")
        print("3. Railway部署")
        print("4. Render部署")
        choice = input("请输入选项 (1-4): ").strip()
        
        deploy_type_map = {
            '1': 'local',
            '2': 'server',
            '3': 'railway',
            '4': 'render'
        }
        deploy_type = deploy_type_map.get(choice, 'local')
    
    if deploy_type == 'local':
        success = deploy_local()
    elif deploy_type == 'server':
        host = os.getenv('DEPLOY_HOST') or input("服务器地址: ").strip()
        user = os.getenv('DEPLOY_USER') or input("用户名: ").strip()
        key_path = os.getenv('DEPLOY_KEY') or input("SSH密钥路径 (可选): ").strip() or None
        success = deploy_to_server(host, user, key_path)
    elif deploy_type == 'railway':
        success = deploy_railway()
    elif deploy_type == 'render':
        success = deploy_render()
    else:
        print("❌ 未知的部署类型")
        sys.exit(1)
    
    if success:
        print()
        print("=" * 60)
        print("✅ 部署成功！")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("❌ 部署失败，请检查错误信息")
        print("=" * 60)
        sys.exit(1)

if __name__ == '__main__':
    main()

