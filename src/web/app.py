"""
AI测试用例生成器 - Web界面
"""

import streamlit as st
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.test_agent import TestAgent
from src.generators.test_case_generator import TestCaseGenerator
from src.generators.data_generator import DataGenerator
from src.config.settings import Settings

# 页面配置
st.set_page_config(
    page_title="QENG AI Automation Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 检查配置
@st.cache_resource
def check_configuration():
    """检查配置是否正确"""
    settings = Settings()
    return settings.validate_api_key()

# 初始化组件
@st.cache_resource
def initialize_components():
    """初始化AI组件"""
    try:
        agent = TestAgent()
        test_generator = TestCaseGenerator()
        data_generator = DataGenerator()
        return agent, test_generator, data_generator, None
    except Exception as e:
        return None, None, None, str(e)

def main():
    """主应用入口"""
    
    # 页面标题
    st.title("🤖 QENG AI Automation Framework")
    st.markdown("QENG AI助手")
    
    # 检查配置
    if not check_configuration():
        st.error("❌ 请先配置Google API密钥")
        st.markdown("""
        请在项目根目录创建 `.env` 文件，并添加以下内容：
        ```
        GOOGLE_API_KEY=your_google_api_key_here
        ```
        """)
        return
    
    # 初始化组件
    agent, test_generator, data_generator, error = initialize_components()
    if error:
        st.error(f"❌ 初始化失败：{error}")
        return
    
    # 侧边栏
    with st.sidebar:
        st.header("功能选择")
        mode = st.selectbox(
            "选择使用模式",
            ["💬 智能对话", "📝 测试用例生成", "🔧 测试数据生成", "📊 批量处理"]
        )
        
        st.markdown("---")
        st.markdown("### 💡 使用提示")
        st.markdown("""
        - **智能对话**：与AI直接交流，描述需求
        - **测试用例生成**：输入功能描述生成测试用例
        - **测试数据生成**：选择数据类型生成测试数据
        - **批量处理**：上传文件批量生成
        """)
    
    # 主内容区域
    if mode == "💬 智能对话":
        chat_interface(agent)
    elif mode == "📝 测试用例生成":
        test_case_interface(test_generator)
    elif mode == "🔧 测试数据生成":
        test_data_interface(data_generator)
    elif mode == "📊 批量处理":
        batch_interface(test_generator, data_generator)

def chat_interface(agent):
    """智能对话界面"""
    st.header("💬 智能对话模式")
    
    # 初始化会话状态
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 显示对话历史
    chat_container = st.container()
    with chat_container:
        for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(user_msg)
            with st.chat_message("assistant"):
                # 显示AI的回复
                st.write(ai_response.get("response"))
                
                # 如果有上下文，则在可扩展组件中显示
                if ai_response.get("context"):
                    with st.expander("🔍 查看检索上下文"):
                        st.markdown(ai_response.get("context"))
    
    # 用户输入
    user_input = st.chat_input("请输入您的需求...")
    
    if user_input:
        # 显示用户消息
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)
        
        # 生成AI响应
        with st.spinner("🤔 AI正在思考..."):
            try:
                response_data = agent.chat(user_input)
                
                # 显示AI响应
                with chat_container:
                    with st.chat_message("assistant"):
                        st.write(response_data.get("response"))
                        # 如果有上下文，则在可扩展组件中显示
                        # if response_data.get("context"):
                        #     with st.expander("🔍 查看检索上下文"):
                                # st.markdown(response_data.get("context"))
                
                # 保存到会话历史
                st.session_state.chat_history.append((user_input, response_data))
                
            except Exception as e:
                st.error(f"处理请求时出现错误：{str(e)}")
    
    # 清空对话按钮
    if st.button("🗑️ 清空对话"):
        st.session_state.chat_history = []
        st.experimental_rerun()

def test_case_interface(test_generator):
    """测试用例生成界面"""
    st.header("📝 测试用例生成")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("功能描述")
        
        # 预设示例
        example_features = [
            "Get Request to API",
            "Get Request to API with Parameters",
            "Post Request to API",
            "Post Request to API with JSON Body",
            "Post Request to API with Form Data",
        ]
        
        selected_example = st.selectbox("选择示例功能", ["自定义"] + example_features)
        
        if selected_example != "自定义":
            feature_description = selected_example
        else:
            feature_description = st.text_area(
                "请输入功能描述",
                placeholder="例如：用户登录功能，包括用户名密码验证、记住登录状态等...",
                height=150
            )
        
        test_framework = st.selectbox(
            "选择测试框架",
            ["pytest", "unittest", "jest", "selenium"]
        )
        
        generate_button = st.button("🚀 生成测试用例", type="primary")
    
    with col2:
        st.subheader("生成结果")
        
        if generate_button and feature_description:
            with st.spinner("⚡ 正在生成测试用例..."):
                try:
                    test_cases = test_generator.generate_from_description(feature_description, test_framework)
                    st.markdown(test_cases)
                    
                    # 下载按钮
                    st.download_button(
                        label="📄 下载测试用例",
                        data=test_cases,
                        file_name=f"test_cases_{feature_description[:10]}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"生成测试用例时出现错误：{str(e)}")
        elif generate_button:
            st.warning("请输入功能描述")

def test_data_interface(data_generator):
    """测试数据生成界面"""
    st.header("🔧 测试数据生成")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("数据配置")
        
        data_types = ['user', 'product', 'order', 'company', 'address', 'payment', 'review', 'article']
        data_type = st.selectbox("选择数据类型", data_types)
        
        count = st.slider("生成数量", min_value=1, max_value=100, value=10)
        
        generate_button = st.button("🔧 生成测试数据", type="primary")
        
        # 数据类型说明
        st.markdown("### 数据类型说明")
        data_descriptions = {
            'user': '👤 用户数据：姓名、邮箱、电话等',
            'product': '📦 产品数据：商品信息、价格、库存等',
            'order': '🛒 订单数据：订单详情、支付信息等',
            'company': '🏢 公司数据：企业信息、联系方式等',
            'address': '📍 地址数据：详细地址、邮编等',
            'payment': '💳 支付数据：交易记录、支付方式等',
            'review': '⭐ 评论数据：用户评价、评分等',
            'article': '📄 文章数据：标题、内容、作者等'
        }
        
        for dtype, desc in data_descriptions.items():
            if dtype == data_type:
                st.info(desc)
    
    with col2:
        st.subheader("生成结果")
        
        if generate_button:
            with st.spinner("🔧 正在生成测试数据..."):
                try:
                    test_data = data_generator.generate_data(data_type, count)
                    
                    # 显示JSON数据
                    st.json(json.loads(test_data))
                    
                    # 下载按钮
                    st.download_button(
                        label="💾 下载测试数据",
                        data=test_data,
                        file_name=f"test_data_{data_type}_{count}.json",
                        mime="application/json"
                    )
                    
                except Exception as e:
                    st.error(f"生成测试数据时出现错误：{str(e)}")

def batch_interface(test_generator, data_generator):
    """批量处理界面"""
    st.header("📊 批量处理")
    
    tab1, tab2 = st.tabs(["📝 批量生成测试用例", "🔧 批量生成测试数据"])
    
    with tab1:
        st.subheader("批量测试用例生成")
        
        uploaded_file = st.file_uploader("上传功能描述文件", type=['txt'])
        
        output_format = st.selectbox("输出格式", ["json", "yaml", "txt"])
        
        if uploaded_file is not None:
            content = str(uploaded_file.read(), "utf-8")
            st.text_area("文件内容预览", content, height=150)
            
            if st.button("🚀 批量生成", type="primary"):
                with st.spinner("⚡ 正在批量生成测试用例..."):
                    try:
                        result = test_generator.generate_from_features(content, output_format)
                        
                        if output_format == "json":
                            st.json(json.loads(result))
                        else:
                            st.text(result)
                        
                        st.download_button(
                            label="📄 下载结果",
                            data=result,
                            file_name=f"batch_test_cases.{output_format}",
                            mime="application/json" if output_format == "json" else "text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"批量生成时出现错误：{str(e)}")
    
    with tab2:
        st.subheader("批量测试数据生成")
        
        st.info("可以同时生成多种类型的测试数据")
        
        data_types = st.multiselect(
            "选择数据类型",
            ['user', 'product', 'order', 'company', 'address', 'payment', 'review', 'article'],
            default=['user', 'product']
        )
        
        count_per_type = st.slider("每种类型生成数量", min_value=1, max_value=50, value=10)
        
        if st.button("🔧 批量生成数据", type="primary"):
            if data_types:
                with st.spinner("🔧 正在批量生成测试数据..."):
                    try:
                        all_data = {}
                        for data_type in data_types:
                            data = data_generator.generate_data(data_type, count_per_type)
                            all_data[data_type] = json.loads(data)
                        
                        st.json(all_data)
                        
                        st.download_button(
                            label="💾 下载所有数据",
                            data=json.dumps(all_data, ensure_ascii=False, indent=2),
                            file_name="batch_test_data.json",
                            mime="application/json"
                        )
                        
                    except Exception as e:
                        st.error(f"批量生成数据时出现错误：{str(e)}")
            else:
                st.warning("请选择至少一种数据类型")

if __name__ == "__main__":
    main()