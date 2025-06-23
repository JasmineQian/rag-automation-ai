"""
AI测试代理 - 核心对话和功能分发模块
"""

import os
from typing import Dict, List, Optional
from ..generators.test_case_generator import TestCaseGenerator
from ..generators.data_generator import DataGenerator
from ..config.settings import Settings
from ..utils.llama_client import LlamaClient
from ..rag.retriever import Retriever

class TestAgent:
    """AI测试代理 - 智能测试助手"""
    
    def __init__(self):
        self.settings = Settings()
        # 配置LLaMA客户端
        self.llama_client = LlamaClient()
        self.test_case_generator = TestCaseGenerator()
        self.data_generator = DataGenerator()
        self.conversation_history = []
        # 初始化RAG检索器
        self.retriever = Retriever()
        
    def chat(self, user_input: str) -> Dict:
        """处理用户输入并返回包含响应和上下文的字典"""
        try:
            # 判断用户意图
            intent = self._analyze_intent(user_input)
            
            # 根据意图调用相应功能
            if intent == "generate_test_cases":
                response = self._handle_test_case_generation(user_input)
                return {"response": response, "context": None}
            elif intent == "generate_test_data":
                response = self._handle_test_data_generation(user_input)
                return {"response": response, "context": None}
            elif intent == "general_chat":
                return self._handle_general_chat(user_input)
            else:
                response = self._handle_help()
                return {"response": response, "context": None}
                
        except Exception as e:
            return {"response": f"抱歉，处理您的请求时出现错误：{str(e)}", "context": None}
    
    def _analyze_intent(self, user_input: str) -> str:
        """分析用户意图"""
        user_input_lower = user_input.lower()
        
        # 测试用例生成相关关键词
        test_case_keywords = ['测试用例', '测试', 'test case', 'feature', '功能测试', '生成测试']
        if any(keyword in user_input_lower for keyword in test_case_keywords):
            return "generate_test_cases"
        
        # 测试数据生成相关关键词
        test_data_keywords = ['测试数据', 'test data', '数据生成', '模拟数据', '假数据']
        if any(keyword in user_input_lower for keyword in test_data_keywords):
            return "generate_test_data"
        
        # 方法系统提示
        help_keywords = ['帮助', 'help', '怎么用', '功能', '使用方法']
        if any(keyword in user_input_lower for keyword in help_keywords):
            return "help"
        
        return "general_chat"
    
    def _handle_test_case_generation(self, user_input: str) -> str:
        """处理测试用例生成请求"""
        try:
            # 提取功能描述
            feature_description = self._extract_feature_description(user_input)
            
            if not feature_description:
                return "请提供具体的功能描述，例如：'为用户登录功能生成测试用例'"
            
            # 生成测试用例
            test_cases = self.test_case_generator.generate_from_description(feature_description)
            
            return f"✅ 根据您的功能描述，我为您生成了以下测试用例：\n\n{test_cases}"
            
        except Exception as e:
            return f"生成测试用例时出现错误：{str(e)}"
    
    def _handle_test_data_generation(self, user_input: str) -> str:
        """处理测试数据生成请求"""
        try:
            # 提取数据类型和数量
            data_info = self._extract_data_info(user_input)
            
            test_data = self.data_generator.generate_data(
                data_info.get('type', 'user'),
                data_info.get('count', 5)
            )
            
            return f"✅ 为您生成了 {data_info.get('count', 5)} 条 {data_info.get('type', 'user')} 类型的测试数据：\n\n{test_data}"
            
        except Exception as e:
            return f"生成测试数据时出现错误：{str(e)}"
    
    def _handle_general_chat(self, user_input: str) -> Dict:
        """处理一般对话，并使用RAG增强上下文"""
        try:
            # 1. 从知识库检索相关上下文
            retrieved_context = self.retriever.query(user_input)
            
            # 2. 构建增强的提示
            system_prompt = """你是一个专业的AI测试助手。请根据下面提供的"相关上下文"来回答用户的问题。如果上下文中没有相关信息，请根据你的通用知识回答，并说明信息并非来自知识库。"""
            
            enhanced_prompt = f"""
相关上下文:
---
{retrieved_context}
---

用户问题: {user_input}
"""
            
            # 3. 使用LLaMA生成响应
            response = self.llama_client.generate_content(enhanced_prompt, system_prompt)
            return {"response": response, "context": retrieved_context}
            
        except Exception as e:
            return {"response": f"对话处理出现错误：{str(e)}", "context": None}
    
    def _handle_help(self) -> str:
        """返回帮助信息"""
        help_text = """
🤖 AI测试用例生成器 - 使用指南

📝 **测试用例生成**
- "为用户登录功能生成测试用例"
- "生成购物车结算的测试用例"
- "帮我写API接口的测试用例"

🔧 **测试数据生成**
- "生成10条用户测试数据"
- "创建产品信息的测试数据"
- "我需要订单数据来测试"

💬 **其他功能**
- 询问测试相关问题
- 讨论测试策略和方法
- 获取测试最佳实践建议

📖 更多帮助请访问项目文档或输入具体的功能需求。
        """
        return help_text.strip()
    
    def _extract_feature_description(self, user_input: str) -> str:
        """从用户输入中提取功能描述"""
        # 简单的关键词提取，实际项目中可以使用更复杂的NLP技术
        keywords_to_remove = ['生成测试用例', '测试用例', '帮我', '请', '为', '的']
        
        description = user_input
        for keyword in keywords_to_remove:
            description = description.replace(keyword, '')
        
        return description.strip()
    
    def _extract_data_info(self, user_input: str) -> Dict:
        """从用户输入中提取数据生成信息"""
        # 提取数量
        import re
        count_match = re.search(r'(\d+)条?', user_input)
        count = int(count_match.group(1)) if count_match else 5
        
        # 提取数据类型
        data_type = 'user'  # 默认用户数据
        if '用户' in user_input:
            data_type = 'user'
        elif '产品' in user_input or '商品' in user_input:
            data_type = 'product'
        elif '订单' in user_input:
            data_type = 'order'
        
        return {'type': data_type, 'count': count} 