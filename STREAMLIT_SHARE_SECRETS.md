# Streamlit Share 密钥配置指南

## 环境变量需求

项目需要以下环境变量来正常运行 LLM 相关功能：

- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `DEEPSEEK_BASE_URL`: DeepSeek API 基础 URL（可选，默认值：`https://api.deepseek.com/v1`）

## 在 Streamlit Share 上配置 Secrets

1. **登录 Streamlit Share**
   - 访问 [https://share.streamlit.io/](https://share.streamlit.io/)
   - 使用 GitHub 账号登录

2. **部署应用**
   - 点击右上角的 "New app" 按钮
   - 选择你的 GitHub 仓库 `ligap123/spam-classification`
   - 选择分支（通常是 `main` 或 `master`）
   - 指定主文件路径：`src/streamlit_app.py`

3. **配置 Secrets**
   - 在部署页面的 "Advanced settings" 部分，点击 "Secrets"
   - 在 Secrets 编辑器中，添加以下内容：

     ```toml
     # DeepSeek API 配置
     DEEPSEEK_API_KEY = "your-deepseek-api-key-here"
     DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
     ```

   - 将 `your-deepseek-api-key-here` 替换为你实际的 DeepSeek API 密钥

4. **完成部署**
   - 点击 "Deploy!" 按钮
   - 等待应用部署完成

## 验证配置

部署完成后，应用将自动使用 Streamlit Share 提供的环境变量。你可以通过以下方式验证：

1. 打开部署后的应用
2. 输入一条短信进行分析
3. 如果配置正确，LLM 分析功能应该能够正常工作

## 注意事项

- **保密密钥**：不要将 API 密钥直接硬编码在代码中或提交到 GitHub
- **环境变量优先级**：Streamlit Share 提供的 Secrets 会覆盖 `.env` 文件中的设置
- **部署后修改**：如果需要修改 Secrets，可以在 Streamlit Share 仪表板中进入应用的 "Settings"，然后在 "Secrets" 部分进行修改
- **API 限制**：确保你的 DeepSeek API 密钥有足够的配额来支持应用使用

## 故障排除

如果应用无法正常使用 LLM 功能，请检查：

1. API 密钥是否正确
2. API 密钥是否有足够的配额
3. 网络连接是否正常
4. DeepSeek API 是否正常运行

你可以在应用的 "Manage app" 页面查看日志，以获取更多调试信息。