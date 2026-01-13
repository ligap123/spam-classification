# 垃圾短信分类系统部署指南

本指南提供多种部署方案，帮助您将垃圾短信分类系统部署为可访问的网站。

## 方案一：Streamlit Community Cloud（推荐，免费）

### 准备工作
1. 将项目上传到GitHub仓库
2. 确保仓库包含以下文件：
   - `src/streamlit_app.py` - 主应用文件
   - `requirements.txt` - 依赖文件
   - `models/` - 包含所有模型文件
   - `.env.example` - 环境变量示例

### 部署步骤

1. **登录Streamlit Community Cloud**
   - 访问 https://share.streamlit.io/
   - 使用GitHub账号登录

2. **创建新应用**
   - 点击"New app"按钮
   - 选择您的GitHub仓库
   - 选择分支（通常是main/master）
   - 设置文件路径：`src/streamlit_app.py`

3. **配置环境变量**
   - 点击"Advanced settings..."
   - 在"Secrets"标签下，添加您的环境变量：
     ```
     DEEPSEEK_API_KEY=your_api_key_here
     ```
   - 点击"Save"

4. **部署应用**
   - 点击"Deploy!"
   - 等待部署完成（通常需要1-5分钟）

5. **访问应用**
   - 部署完成后，您将获得一个URL（格式：https://your-app.streamlit.app）
   - 您可以通过此URL访问应用，手机和电脑都可以使用

### 注意事项
- Streamlit Community Cloud提供免费部署，但有资源限制
- 应用可能在一段时间不使用后自动休眠
- 环境变量存储在安全的Secrets管理器中，不会暴露

## 方案二：Docker容器化部署

### 准备工作
1. 安装Docker
2. 确保项目包含所有必要文件

### 创建Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/streamlit_app.py"]
```

### 构建和运行容器
```bash
# 构建镜像
docker build -t spam-classification .

# 运行容器
docker run -d -p 8501:8501 --env-file .env spam-classification
```

### 访问应用
- 本地访问：http://localhost:8501
- 如果部署在服务器上，访问：http://服务器IP:8501

## 方案三：AWS EC2部署

### 准备工作
1. 拥有AWS账号
2. 创建EC2实例（推荐使用t2.medium或更高配置）

### 部署步骤

1. **连接到EC2实例**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **安装依赖**
   ```bash
   sudo apt update
   sudo apt install python3-pip git docker.io -y
   sudo systemctl start docker
   sudo usermod -aG docker ubuntu
   ```

3. **克隆仓库**
   ```bash
   git clone your-github-repo-url
   cd spam-classification
   ```

4. **构建和运行Docker容器**
   ```bash
   docker build -t spam-classification .
   docker run -d -p 80:8501 --env-file .env spam-classification
   ```

5. **配置安全组**
   - 在AWS控制台中，为EC2实例添加安全组规则
   - 允许HTTP流量（端口80）

6. **访问应用**
   - 访问：http://your-ec2-ip

## 方案四：GCP App Engine部署

### 准备工作
1. 拥有GCP账号
2. 安装gcloud CLI

### 创建app.yaml文件
```yaml
runtime: python312
env: standard

instance_class: F2

handlers:
- url: /.*
  script: auto
  secure: always
  redirect_http_response_code: 301

env_variables:
  DEEPSEEK_API_KEY: "your_api_key_here"

entrypoint: streamlit run src/streamlit_app.py --server.port $PORT
```

### 部署步骤
```bash
# 初始化gcloud
gcloud init

# 部署应用
gcloud app deploy

# 查看应用
gcloud app browse
```

## 环境变量配置

无论选择哪种部署方案，都需要配置以下环境变量：

- **DEEPSEEK_API_KEY**：DeepSeek API密钥，用于LLM功能

### 本地开发
创建`.env`文件：
```
DEEPSEEK_API_KEY=your_api_key_here
```

### 生产部署
根据部署平台的要求配置环境变量：
- Streamlit Community Cloud：使用Secrets管理器
- Docker：使用`--env-file`参数
- AWS/GCP：使用平台提供的环境变量配置功能

## 测试部署后的应用

1. **功能测试**
   - 输入示例短信进行分类
   - 测试模型对比功能
   - 检查LLM分析结果

2. **性能测试**
   - 测试应用加载速度
   - 测试分类响应时间

3. **兼容性测试**
   - 在不同浏览器中测试
   - 在手机和电脑上测试

## 维护和更新

1. **更新代码**
   - Streamlit Community Cloud：推送代码到GitHub，自动更新
   - Docker：重新构建镜像并运行
   - AWS/GCP：重新部署应用

2. **更新模型**
   - 重新训练模型
   - 替换models/目录下的模型文件
   - 重新部署应用

3. **监控应用**
   - Streamlit Community Cloud：使用内置监控
   - 其他平台：配置日志监控

---

祝您部署顺利！如果遇到问题，请参考相应平台的官方文档或联系技术支持。