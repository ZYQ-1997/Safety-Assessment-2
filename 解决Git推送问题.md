# 解决Git推送权限问题

## 问题：Permission denied (publickey)

这是因为GitHub需要SSH密钥认证，但您还没有配置SSH密钥。

## 解决方案（3种方法）

### 方法1: 改用HTTPS方式（最简单，推荐）

**步骤：**

1. **查看当前远程仓库地址**：
   ```bash
   git remote -v
   ```

2. **将SSH地址改为HTTPS地址**：
   ```bash
   # 如果当前是：git@github.com:用户名/仓库名.git
   # 改为：https://github.com/用户名/仓库名.git
   
   git remote set-url origin https://github.com/您的用户名/您的仓库名.git
   ```

3. **重新推送**：
   ```bash
   git push origin main
   ```

4. **输入GitHub用户名和密码**（或Personal Access Token）

### 方法2: 配置SSH密钥（一次性配置）

**步骤：**

1. **生成SSH密钥**（如果还没有）：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # 按回车使用默认位置
   # 可以设置密码或直接回车（不设置密码）
   ```

2. **复制公钥**：
   ```bash
   # Windows (Git Bash)
   cat ~/.ssh/id_ed25519.pub
   
   # 或者Windows PowerShell
   type $env:USERPROFILE\.ssh\id_ed25519.pub
   ```

3. **添加到GitHub**：
   - 访问：https://github.com/settings/keys
   - 点击 "New SSH key"
   - Title: 随意填写（如：My Computer）
   - Key: 粘贴刚才复制的公钥
   - 点击 "Add SSH key"

4. **测试连接**：
   ```bash
   ssh -T git@github.com
   ```

5. **重新推送**：
   ```bash
   git push origin main
   ```

### 方法3: 使用GitHub Desktop（最简单，推荐）

**如果您不想配置SSH密钥，使用GitHub Desktop最简单：**

1. **下载GitHub Desktop**：https://desktop.github.com
2. **安装并登录GitHub账号**
3. **打开GitHub Desktop**
4. **点击 "File" → "Add Local Repository"**
5. **选择项目文件夹**
6. **点击 "Publish repository"**（如果是新仓库）
   - 或点击 "Push origin"（如果已存在远程仓库）

GitHub Desktop会自动处理认证，无需配置SSH密钥！

## 推荐方案

**最简单的方式**：使用GitHub Desktop
- 无需配置SSH密钥
- 图形界面，操作简单
- 自动处理认证

**或者**：改用HTTPS方式
- 只需修改远程仓库地址
- 使用用户名和密码（或Token）推送

## 使用Personal Access Token（如果HTTPS需要）

如果使用HTTPS方式，GitHub可能要求使用Personal Access Token而不是密码：

1. **生成Token**：
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token" → "Generate new token (classic)"
   - 设置名称和过期时间
   - 勾选 `repo` 权限
   - 点击 "Generate token"
   - **复制Token**（只显示一次！）

2. **使用Token推送**：
   ```bash
   git push origin main
   # 用户名：您的GitHub用户名
   # 密码：粘贴刚才复制的Token
   ```

## 快速修复命令

**如果您知道仓库地址，直接运行：**

```bash
# 将SSH地址改为HTTPS（替换为您的实际仓库地址）
git remote set-url origin https://github.com/您的用户名/您的仓库名.git

# 然后推送
git push origin main
```

## 需要帮助？

如果还有问题，请告诉我：
1. 您的GitHub用户名
2. 仓库名称
3. 您想使用哪种方法（HTTPS、SSH、或GitHub Desktop）

我可以帮您具体操作！

