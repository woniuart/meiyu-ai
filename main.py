"""
MEIYU-AI 全校美育智能体
Multi-Module AI Art Education Assistant for Universities

核心模块：
1. 艺术心理疗愈 - 情绪识别 + 绘画/音乐/戏剧疗愈
2. 美术美育 - AI创作 + 艺术鉴赏
3. 音乐美育 - 音乐创作 + 鉴赏
4. 舞蹈美育 - AI舞蹈教学
5. 戏剧美育 - 即兴戏剧 + 剧本创作
6. 社交美育 - 艺术社交 + 兴趣匹配
"""

import os
import json
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# AG2 and OpenAI imports
from autogen.agentchat import ConversableAgent, AssistantAgent, Agent
from autogen import OpenAIWrapper, AgentRuntime
from autogen.agentchat.group import GroupChat, GroupChatManager

# Streamlit for web UI
import streamlit as st
import pandas as pd

# ============== Configuration ==============

class Config:
    """MEIYU-AI Configuration"""
    
    # SiliconFlow API (Free tier available)
    API_KEY = os.getenv("SILICONFLOW_API_KEY", "sk-mdoklwrqimsbvjnruqrsdxmzoaycpekndmyvqgyymfqwooqa")
    BASE_URL = "https://api.siliconflow.cn/v1"
    MODEL = "Pro/Qwen/Qwen2-72B-Instruct"
    
    # For image analysis
    VISION_MODEL = "Qwen/Qwen2-VL-72B-Instruct"
    
    # App Configuration
    APP_TITLE = "MEIYU-AI 全校美育智能体"
    APP_ICON = "🎨"
    VERSION = "1.0.0"
    
    # Session state keys
    KEY_CHAT_HISTORY = "chat_history"
    KEY_CURRENT_MODULE = "current_module"
    KEY_USER_PROFILE = "user_profile"
    KEY_EMOTION_STATE = "emotion_state"


# ============== User Profile & State ==============

@dataclass
class UserProfile:
    """User profile for personalized recommendations"""
    user_id: str = ""
    name: str = ""
    interests: List[str] = field(default_factory=list)
    preferred_art_forms: List[str] = field(default_factory=list)
    emotional_history: List[Dict] = field(default_factory=list)
    interaction_count: int = 0


@dataclass
class EmotionState:
    """Current emotional state of the user"""
    primary_emotion: str = "neutral"  # happy, sad, anxious, angry, neutral
    intensity: float = 0.5  # 0-1 scale
    suggested_activities: List[str] = field(default_factory=list)
    last_updated: str = ""


# ============== Agent System ==============

class AgentFactory:
    """Factory for creating MEIYU-AI specialized agents"""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm_config = {
            "model": config.MODEL,
            "api_key": config.API_KEY,
            "base_url": config.BASE_URL,
            "temperature": 0.7,
            "max_tokens": 2000,
        }
    
    def create_system_message(self, role: str, expertise: str, tone: str) -> str:
        """Create system message for an agent"""
        return f"""你是MEIYU-AI美育智能体的{role}。
{expertise}
{tone}

请始终保持温暖、专业、耐心的态度。
根据用户的需求提供个性化的美育体验。
避免使用专业心理术语，用通俗易懂的艺术语言来帮助用户。"""

    def create_art_therapy_agent(self) -> ConversableAgent:
        """Create Art Therapy Agent - 艺术心理疗愈模块"""
        system_msg = self.create_system_message(
            role="艺术心理疗愈导师",
            expertise="""你是专业的艺术疗愈专家，擅长通过艺术方式帮助学生缓解情绪压力。
你掌握以下疗愈技术：
- 绘画疗愈：曼陀罗涂色、自由创作、情绪转化
- 音乐疗愈：情绪歌单、呼吸训练、声音疗愈
- 戏剧疗愈：角色扮演、空椅子技术、故事改写

你能够：
- 通过对话识别用户情绪状态
- 推荐适合的艺术疗愈活动
- 引导用户进行艺术表达
- 分析用户作品中的情绪元素""",
            tone="你说话温柔、有同理心，像一个大姐姐/大哥哥。不评价用户的创作好坏，而是关注他们的情感表达。"
        )
        
        return ConversableAgent(
            name="艺术疗愈导师",
            system_message=system_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )
    
    def create_art_education_agent(self) -> ConversableAgent:
        """Create Art Education Agent - 美术美育模块"""
        system_msg = self.create_system_message(
            role="美术教育导师",
            expertise="""你是专业的美术教育专家，擅长引导零基础学生发现艺术之美。
你掌握：
- 艺术史知识：从古典到现代、从东方到西方
- 数字艺术创作：AI绘画、风格迁移、图像编辑
- 艺术鉴赏：作品解读、文化背景分析

你能够：
- 用通俗有趣的方式讲解艺术史
- 引导用户进行艺术创作
- 解读经典作品的艺术价值
- 帮助用户找到自己的艺术风格""",
            tone="你热情洋溢，善于发现用户作品中的亮点。鼓励用户大胆创作，不强调技巧，而是表达自我。"
        )
        
        return ConversableAgent(
            name="美术导师",
            system_message=system_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )
    
    def create_music_education_agent(self) -> ConversableAgent:
        """Create Music Education Agent - 音乐美育模块"""
        system_msg = self.create_system_message(
            role="音乐教育导师",
            expertise="""你是专业的音乐教育专家，让音乐成为用户生活的一部分。
你掌握：
- 音乐理论：旋律、和声、节奏
- 音乐风格：古典、爵士、摇滚、电子、流行
- 音乐创作：作曲、编曲、混音基础
- 音乐鉴赏：聆听技巧、音乐分析

你能够：
- 介绍不同音乐风格的特点
- 根据用户情绪推荐音乐
- 引导用户进行简单音乐创作
- 解读歌词和音乐背后的故事""",
            tone="你热爱音乐，善于用音乐来表达情感。鼓励用户多听、多感受，不强行灌输知识。"
        )
        
        return ConversableAgent(
            name="音乐导师",
            system_message=system_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )
    
    def create_dance_education_agent(self) -> ConversableAgent:
        """Create Dance Education Agent - 舞蹈美育模块"""
        system_msg = self.create_system_message(
            role="舞蹈教育导师",
            expertise="""你是专业的舞蹈教育专家，让每个人都能享受舞蹈的乐趣。
你掌握：
- 舞蹈风格：流行舞（K-pop、街舞、爵士）、古典舞、健身舞、民族舞
- 舞蹈教学：动作分解、节奏把握、表情管理
- 舞蹈文化：各舞种的历史和文化背景

你能够：
- 介绍不同舞蹈风格的特点
- 提供基础舞蹈动作教学
- 根据用户身体条件推荐适合的舞蹈
- 鼓励用户自信地展现自我""",
            tone="你充满活力，表演欲强。强调舞蹈是一种表达自我的方式，不是炫技。"
        )
        
        return ConversableAgent(
            name="舞蹈导师",
            system_message=system_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )
    
    def create_drama_education_agent(self) -> ConversableAgent:
        """Create Drama Education Agent - 戏剧美育模块"""
        system_msg = self.create_system_message(
            role="戏剧教育导师",
            expertise="""你是专业的戏剧教育专家，通过戏剧提升用户的表达能力和共情能力。
你掌握：
- 即兴戏剧：各种即兴游戏和表演技巧
- 戏剧创作：剧本写作、角色塑造、舞台调度
- 经典剧目：中西方经典戏剧作品分析
- 表演技巧：台词、表情、肢体语言

你能够：
- 引导用户进行即兴表演
- 帮助用户创作自己的剧本
- 分析经典戏剧作品
- 提升用户的表达自信""",
            tone="你戏感十足，善于引导用户释放表演欲。强调戏剧是一种安全的自我探索方式。"
        )
        
        return ConversableAgent(
            name="戏剧导师",
            system_message=system_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )
    
    def create_social_education_agent(self) -> ConversableAgent:
        """Create Social Art Education Agent - 社交美育模块"""
        system_msg = self.create_system_message(
            role="社交美育导师",
            expertise="""你是社交美育专家，帮助大学生通过艺术建立真实、有深度的社交关系。
你掌握：
- 艺术社交：共同创作、艺术活动、艺术兴趣小组
- 社交技巧：破冰话题、相处之道、冲突化解
- 活动策划：线上艺术活动、线下聚会组织

你能够：
- 根据用户兴趣推荐艺术活动
- 提供社交破冰建议
- 引导用户参与集体艺术创作
- 帮助用户找到志同道合的艺术伙伴""",
            tone="你善解人意，理解大学生的社恐心理。用艺术作为安全的社交媒介，降低社交门槛。"
        )
        
        return ConversableAgent(
            name="社交导师",
            system_message=system_msg,
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )


# ============== Main Application ==============

class MEIYUAIBot:
    """Main MEIYU-AI Bot Application"""
    
    def __init__(self):
        self.config = Config()
        self.factory = AgentFactory(self.config)
        
        # Initialize agents
        self.agents = {
            "art_therapy": self.factory.create_art_therapy_agent(),
            "art_education": self.factory.create_art_education_agent(),
            "music_education": self.factory.create_music_education_agent(),
            "dance_education": self.factory.create_dance_education_agent(),
            "drama_education": self.factory.create_drama_education_agent(),
            "social_education": self.factory.create_social_education_agent(),
        }
    
    def get_module_info(self, module_key: str) -> Dict[str, str]:
        """Get module information"""
        modules = {
            "art_therapy": {
                "name": "艺术心理疗愈",
                "icon": "💆",
                "description": "用艺术治愈心灵 - 绘画疗愈、音乐疗愈、戏剧疗愈",
                "color": "#E8F5E9",
            },
            "art_education": {
                "name": "美术美育",
                "icon": "🎨",
                "description": "AI艺术创作 + 经典作品鉴赏",
                "color": "#FFF3E0",
            },
            "music_education": {
                "name": "音乐美育",
                "icon": "🎵",
                "description": "音乐创作实验室 + 沉浸式音乐体验",
                "color": "#E1F5FE",
            },
            "dance_education": {
                "name": "舞蹈美育",
                "icon": "💃",
                "description": "AI舞蹈教学 + 热门舞蹈体验",
                "color": "#FCE4EC",
            },
            "drama_education": {
                "name": "戏剧美育",
                "icon": "🎭",
                "description": "即兴戏剧工坊 + 经典剧目体验",
                "color": "#F3E5F5",
            },
            "social_education": {
                "name": "社交美育",
                "icon": "🤝",
                "description": "艺术兴趣社交 + 协作创作",
                "color": "#E0F2F1",
            },
        }
        return modules.get(module_key, {})
    
    def chat(self, module_key: str, message: str) -> str:
        """Send a message to a specific module agent"""
        if module_key not in self.agents:
            return "抱歉，暂不支持该模块。"
        
        agent = self.agents[module_key]
        
        try:
            # Create a proxy agent for receiving responses
            proxy = ConversableAgent(
                name="user_proxy",
                system_message="你是用户，请直接回应。",
                llm_config=self.config.llm_config,
                human_input_mode="NEVER",
            )
            
            # Initiate chat
            agent.initiate_chat(
                recipient=proxy,
                message=message,
            )
            
            # Get last message from agent
            response = agent.chat_messages.get(proxy, [])
            if response:
                return response[-1].get("content", "抱歉，我暂时不知道如何回答。")
            return "抱歉，我暂时不知道如何回答。"
            
        except Exception as e:
            return f"遇到了一些问题：{str(e)}。请稍后重试或尝试其他模块。"
    
    def get_welcome_message(self, module_key: str) -> str:
        """Get welcome message for a module"""
        welcomes = {
            "art_therapy": """🌸 欢迎来到艺术心理疗愈空间

我是你的艺术疗愈导师 💆
在这里，你可以：
- 聊聊今天的心情，我会用艺术的方式帮助你
- 进行曼陀罗涂色或自由创作
- 聆听为你定制的疗愈音乐
- 通过戏剧角色释放内心情绪

不着急，慢慢来。
现在，告诉我你今天感觉怎么样？""",
            
            "art_education": """🎨 欢迎来到美术美育空间

我是你的美术导师 🎨
在这里，你可以：
- 了解艺术史上的有趣故事
- 用AI创作专属的艺术作品
- 学习鉴赏经典大师作品
- 探索不同的艺术风格

你有特别想了解的艺术风格或作品吗？
或者，让我们一起创作？""",
            
            "music_education": """🎵 欢迎来到音乐美育空间

我是你的音乐导师 🎵
在这里，你可以：
- 了解各种音乐风格的魅力
- 探索一首歌曲背后的故事
- 找到适合当下心情的音乐
- 体验简单的音乐创作

今天想听什么类型的音乐？
或者想了解哪种音乐风格？""",
            
            "dance_education": """💃 欢迎来到舞蹈美育空间

我是你的舞蹈导师 💃
在这里，你可以：
- 学习热门流行舞（K-pop、街舞、爵士）
- 了解古典舞和民族舞的基础
- 跟着节奏动起来，释放活力
- 观看舞蹈视频，获取灵感

想跳什么类型的舞蹈？
或者只是想活动一下身体？""",
            
            "drama_education": """🎭 欢迎来到戏剧美育空间

我是你的戏剧导师 🎭
在这里，你可以：
- 玩即兴戏剧游戏，释放天性
- 创作属于自己的小剧本
- 体验不同角色的悲欢离合
- 了解经典戏剧作品的魅力

想玩游戏，还是想演戏？
或者只是想聊聊戏剧？""",
            
            "social_education": """🤝 欢迎来到社交美育空间

我是你的社交导师 🤝
在这里，你可以：
- 找到志同道合的艺术伙伴
- 参与有趣的集体艺术活动
- 学习社交破冰小技巧
- 发起或加入艺术兴趣小组

想认识有共同兴趣的朋友吗？
还是想参加一些有趣的线上活动？""",
        }
        return welcomes.get(module_key, "欢迎使用MEIYU-AI")


# ============== Streamlit UI ==============

def init_session_state():
    """Initialize Streamlit session state"""
    if Config.KEY_CHAT_HISTORY not in st.session_state:
        st.session_state[Config.KEY_CHAT_HISTORY] = {}
    
    if Config.KEY_CURRENT_MODULE not in st.session_state:
        st.session_state[Config.KEY_CURRENT_MODULE] = "art_therapy"
    
    if "bot" not in st.session_state:
        st.session_state["bot"] = MEIYUAIBot()


def render_sidebar():
    """Render the sidebar with module selection"""
    st.sidebar.title(f"{Config.APP_ICON} MEIYU-AI")
    st.sidebar.caption("全校美育智能体 v" + Config.VERSION)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("选择模块")
    
    bot = st.session_state["bot"]
    modules = [
        ("art_therapy", "💆 艺术心理疗愈"),
        ("art_education", "🎨 美术美育"),
        ("music_education", "🎵 音乐美育"),
        ("dance_education", "💃 舞蹈美育"),
        ("drama_education", "🎭 戏剧美育"),
        ("social_education", "🤝 社交美育"),
    ]
    
    selected_module = st.sidebar.radio(
        "功能模块",
        [m[0] for m in modules],
        format_func=lambda x: next(m[1] for m in modules if m[0] == x),
        index=[m[0] for m in modules].index(st.session_state.get(Config.KEY_CURRENT_MODULE, "art_therapy"))
    )
    
    st.session_state[Config.KEY_CURRENT_MODULE] = selected_module
    
    # Show module description
    module_info = bot.get_module_info(selected_module)
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"<div style='background-color: {module_info.get('color', '#fff')}; padding: 10px; border-radius: 10px;'>"
        f"<b>{module_info.get('icon', '')} {module_info.get('name', '')}</b><br>"
        f"<small>{module_info.get('description', '')}</small>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 提示：这是AI助手，不能替代专业心理咨询。如有严重心理问题，请联系学校心理中心。")
    
    return selected_module


def render_chat_area(module_key: str):
    """Render the main chat area"""
    bot = st.session_state["bot"]
    
    # Initialize module chat history if not exists
    if module_key not in st.session_state[Config.KEY_CHAT_HISTORY]:
        st.session_state[Config.KEY_CHAT_HISTORY][module_key] = [
            {"role": "assistant", "content": bot.get_welcome_message(module_key)}
        ]
    
    chat_history = st.session_state[Config.KEY_CHAT_HISTORY][module_key]
    
    # Display chat messages
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    return chat_history


def handle_user_input(module_key: str, user_input: str):
    """Handle user input and get AI response"""
    bot = st.session_state["bot"]
    chat_history = st.session_state[Config.KEY_CHAT_HISTORY][module_key]
    
    # Add user message to history
    chat_history.append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = bot.chat(module_key, user_input)
            st.markdown(response)
    
    # Add assistant message to history
    chat_history.append({"role": "assistant", "content": response})
    
    # Update session state
    st.session_state[Config.KEY_CHAT_HISTORY][module_key] = chat_history


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    div[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize
    init_session_state()
    
    # Render sidebar
    selected_module = render_sidebar()
    
    # Main content area
    st.title(f"{Config.APP_ICON} {Config.APP_TITLE}")
    
    # Render chat area
    chat_history = render_chat_area(selected_module)
    
    # Chat input
    if prompt := st.chat_input("输入你的问题或想法..."):
        handle_user_input(selected_module, prompt)
        st.rerun()
    
    # Clear chat button
    if st.sidebar.button("清空对话", use_container_width=True):
        st.session_state[Config.KEY_CHAT_HISTORY][selected_module] = [
            {"role": "assistant", "content": st.session_state["bot"].get_welcome_message(selected_module)}
        ]
        st.rerun()


if __name__ == "__main__":
    main()