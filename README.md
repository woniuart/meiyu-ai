# 🎨 MEIYU-AI 全校美育智能体

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![AG2](https://img.shields.io/badge/AG2-AutoGen-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**大学生全维度美育成长陪伴者**

</div>

## 📖 项目简介

MEIYU-AI 是一款基于大语言模型的智能美育助手，旨在为大学生提供"艺术体验+心理疗愈+社交连接+人格塑造"四位一体的美育服务。

### 核心特点

- 🎭 **多模块架构**：艺术心理疗愈、美术、音乐、舞蹈、戏剧、社交六大模块
- 🤖 **AI驱动**：基于 AG2 + Qwen2 大模型，提供智能对话和个性化推荐
- 🌐 **Web部署**：Streamlit 轻量化 Web 应用，支持多终端访问
- 🎓 **教育导向**：专为大学生设计，解决学业压力、社交焦虑等痛点

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│              Streamlit Web UI           │
└─────────┬─────────┬─────────┬─────────┘
          │         │         │
┌─────────▼─┐ ┌─────▼─────┐ ┌▼─────────┐
│ 心理疗愈  │ │ 美术美育  │ │ 音乐美育 │
└───────────┘ └───────────┘ └───────────┘
┌───────────┐ ┌───────────┐ ┌───────────┐
│ 舞蹈美育  │ │ 戏剧美育  │ │ 社交美育 │
└───────────┘ └───────────┘ └───────────┘
          │         │         │
┌─────────▼─────────▼─────────▼─────────┐
│       AG2 Multi-Agent System          │
│  (艺术疗愈导师、美术导师、音乐导师...)  │
└─────────┬─────────┬─────────┬─────────┘
          │         │         │
┌─────────▼─────────▼─────────▼─────────┐
│        SiliconFlow API (Qwen2)        │
└─────────────────────────────────────────┘
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/woniuart/meiyu-ai.git
cd meiyu-ai
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
streamlit run main.py
```

### 4. 访问

打开浏览器访问 http://localhost:8501

## 📱 功能模块

| 模块 | 功能描述 |
|------|---------|
| 💆 艺术心理疗愈 | 情绪识别、绘画疗愈、音乐疗愈、戏剧疗愈 |
| 🎨 美术美育 | AI绘画、艺术鉴赏、风格探索、数字创作 |
| 🎵 音乐美育 | 音乐创作、风格探索、音乐鉴赏、情绪歌单 |
| 💃 舞蹈美育 | AI舞蹈教学、流行舞体验、动作分解 |
| 🎭 戏剧美育 | 即兴戏剧、剧本创作、角色扮演 |
| 🤝 社交美育 | 艺术社交、兴趣匹配、协作创作 |

## 🔧 配置说明

### API 配置

项目默认使用 SiliconFlow API 免费额度。如需自定义：

```bash
# 方式1: 环境变量
export SILICONFLOW_API_KEY="your-api-key"

# 方式2: 直接修改代码
# 编辑 main.py 中的 Config 类
```

### 可用模型

- `Pro/Qwen/Qwen2-72B-Instruct` (默认)
- `Pro/Qwen/Qwen2-VL-72B-Instruct` (视觉理解)

## 🌐 部署

### Render 部署 (推荐)

点击下方按钮一键部署：

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/woniuart/meiyu-ai)

### Railway 部署

```bash
# 1. 安装 Railway CLI
npm i -g @railway/cli

# 2. 登录
railway login

# 3. 初始化
railway init

# 4. 部署
railway up
```

### 本地隧道测试

```bash
# 使用 localtunnel
npx localtunnel --port 8501

# 或使用 ngrok
ngrok http 8501
```

## 📊 发展规划

- [ ] 添加语音交互功能
- [ ] 增加图像生成能力 (AI 绘画)
- [ ] 开发移动端 APP
- [ ] 集成校园身份认证
- [ ] 增加 AR/VR 沉浸式体验
- [ ] 对接学校心理健康系统

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

<div align="center">

Made with ❤️ for Chinese University Students

</div>