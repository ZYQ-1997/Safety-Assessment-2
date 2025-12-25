# Railway 自动部署指南（5分钟完成）

## 步骤1: 准备GitHub仓库

如果您的代码还没有推送到GitHub：

```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit"

# 在GitHub上创建新仓库，然后：
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

## 步骤2: 部署到Railway

1. **访问**: https://railway.app
2. **点击 "Login"** → 选择 "Login with GitHub"
3. **授权Railway访问您的GitHub账户**
4. **点击 "New Project"**
5. **选择 "Deploy from GitHub repo"**
6. **选择您的仓库**
7. **Railway会自动检测Dockerfile并开始部署**

## 步骤3: 配置（可选）

### 设置自定义域名

1. 在Railway项目页面，点击 "Settings"
2. 找到 "Domains" 部分
3. 点击 "Generate Domain" 或添加自定义域名
4. Railway会自动配置HTTPS

### 设置环境变量（如需要）

1. 在项目页面，点击 "Variables"
2. 添加需要的环境变量

## 完成！

部署完成后，Railway会提供一个URL，如：
- `https://your-app.railway.app`

访问这个URL即可使用您的应用！

## 自动更新

每次您推送代码到GitHub的main分支，Railway会自动重新部署。

## 费用

Railway提供：
- **免费额度**: $5/月（足够小型应用使用）
- **按需付费**: 超出免费额度后按实际使用付费

## 故障排除

如果部署失败：
1. 检查Railway的部署日志
2. 确保Dockerfile正确
3. 检查requirements.txt中的依赖

