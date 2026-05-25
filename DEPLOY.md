# MEIYU-AI 部署指南

## 一键部署到 Render（推荐）

### 步骤：
1. 点击下方部署按钮：
   
   **https://render.com/deploy?repo=https://github.com/woniuart/meiyu-ai**

2. 登录 GitHub 授权 Render

3. 按照默认配置创建服务：
   - Name: `meiyu-ai`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run main.py --server.port $PORT --server.address 0.0.0.0`

4. 点击"Create Web Service"

5. 等待2-3分钟构建完成，获取公网URL

### 环境变量配置

在 Render Dashboard 中添加：
- `SILICONFLOW_API_KEY` = `sk-mdoklwrqimsbvjnruqrsdxmzoaycpekndmyvqgyymfqwooqa` （可选，使用默认）

## 本地运行

```bash
# 克隆
git clone https://github.com/woniuart/meiyu-ai.git
cd meiyu-ai

# 安装依赖
pip install -r requirements.txt

# 运行
streamlit run main.py
```

访问 http://localhost:8501

## Railway 部署

```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 初始化
cd meiyu-ai
railway init

# 设置环境变量
railway variables set SILICONFLOW_API_KEY=sk-mdoklwrqimsbvjnruqrsdxmzoaycpekndmyvqgyymfqwooqa

# 部署
railway up
```

## 常见问题

**Q: 部署后无法访问？**
A: 检查 Render 日志，确保所有依赖安装成功

**Q: 响应很慢？**
A: 免费服务器资源有限，建议升级付费套餐

**Q: 需要修改代码？**
A: 修改后推送到 GitHub，Render 会自动重新部署