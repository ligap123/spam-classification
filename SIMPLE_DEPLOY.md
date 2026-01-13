# 简易部署指南：无需命令行

根据您遇到的问题，我整理了一个更简单的部署方案，主要通过网页界面操作，无需复杂的命令行操作。

## 步骤一：手动创建GitHub仓库

### 1. 登录GitHub
- 访问 https://github.com
- 使用您的账号登录

### 2. 创建新仓库
- 点击右上角的"+"，选择"New repository"
- **仓库名称**：输入 `spam-classification`
- **描述**：输入 "SMS Spam Classification with ML and LLM Agent"
- **可见性**：选择 "Public"
- **初始化选项**：不要勾选任何选项（不创建README、.gitignore等）
- 点击 "Create repository"

### 3. 下载GitHub Desktop（可选）
- 如果您不熟悉Git命令行，可以使用GitHub Desktop：
- 下载：https://desktop.github.com/
- 安装并登录GitHub账号

## 步骤二：上传项目文件到GitHub

### 方法A：使用GitHub Desktop
1. **克隆仓库**：
   - 在GitHub Desktop中，点击"Add" → "Clone repository"
   - 选择您刚刚创建的"spam-classification"仓库
   - 选择本地保存位置
   - 点击"Clone"

2. **复制项目文件**：
   - 打开克隆的仓库文件夹
   - 将您的项目文件（f:\机器学习下的所有文件）复制到这个文件夹
   - 确保不包含`.git`、`.venv`、`env`等隐藏或虚拟环境文件夹

3. **提交和推送**：
   - 在GitHub Desktop中，您会看到所有添加的文件
   - 在"Summary"中输入"Initial commit"
   - 点击"Commit to main"
   - 点击"Push origin"

### 方法B：使用浏览器直接上传
1. 在GitHub仓库页面，点击"Add file" → "Upload files"
2. 拖拽所有项目文件到浏览器窗口
3. 在"Commit changes"部分，输入"Initial commit"
4. 点击"Commit changes"

## 步骤三：部署到Streamlit Share

1. **访问Streamlit Share**：
   - 访问 https://share.streamlit.io/
   - 使用GitHub账号登录

2. **创建新应用**：
   - 点击"New app"按钮
   - 在"Repository"下拉菜单中，选择您的`ligap123/spam-classification`仓库
   - 在"Branch"下拉菜单中，选择"main"或"master"
   - 在"Main file path"输入框中，输入`src/streamlit_app.py`

3. **配置环境变量**：
   - 点击"Advanced settings..."
   - 在"Secrets"标签下，添加以下内容：
     ```
     DEEPSEEK_API_KEY=your_api_key_here
     DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
     ```
   - 点击"Save"

4. **部署应用**：
   - 点击"Deploy!"
   - 等待部署完成（通常需要1-5分钟）

5. **访问您的应用**：
   - 部署完成后，您将获得一个URL（格式：https://your-app.streamlit.app）
   - 您可以通过此URL在手机和电脑上访问应用

## 替代方案：使用Heroku部署

如果您在Streamlit Share部署过程中遇到问题，可以尝试使用Heroku：

1. **创建Heroku账号**：访问 https://www.heroku.com/ 并注册

2. **安装Heroku CLI**：
   - 下载：https://devcenter.heroku.com/articles/heroku-cli
   - 安装并登录

3. **创建Procfile**：
   - 在项目根目录创建一个名为`Procfile`的文件
   - 内容：`web: streamlit run --server.port $PORT src/streamlit_app.py`

4. **部署到Heroku**：
   ```bash
   heroku create spam-classification-app
   git push heroku main
   heroku config:set DEEPSEEK_API_KEY=your_api_key_here
   heroku config:set DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
   heroku open
   ```

## 注意事项

- 确保所有必要的文件都已上传到GitHub仓库，特别是`src/streamlit_app.py`、`requirements.txt`和`models/`目录
- 环境变量中的`DEEPSEEK_API_KEY`必须是有效的，否则应用无法正常工作
- 如果部署过程中遇到问题，可以查看部署日志获取更多信息

如果您在任何步骤遇到问题，请随时告诉我，我会提供进一步的帮助。
