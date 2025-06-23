"""
LLaMA客户端 - 与Ollama API通信
"""

import requests
import json
from typing import Dict, Optional
from ..config.settings import Settings

class LlamaClient:
    """LLaMA模型客户端，使用Ollama API"""
    
    def __init__(self):
        self.settings = Settings()
        self.base_url = self.settings.ollama_base_url
        self.model = self.settings.llama_model
        self.temperature = self.settings.model_temperature
        self.max_tokens = self.settings.max_tokens
        
    def generate_content(self, prompt: str, system_prompt: str = None) -> str:
        """生成内容"""
        try:
            # 构建请求数据
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user", 
                "content": prompt
            })
            
            data = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            # 发送请求到Ollama API
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            else:
                return f"API请求失败，状态码: {response.status_code}"
                
        except Exception as e:
            return f"生成内容时出现错误：{str(e)}"
    
    def check_model_availability(self) -> bool:
        """检查模型是否可用"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model.get("name") == self.model for model in models)
            return False
        except:
            return False
    
    def pull_model(self) -> bool:
        """拉取模型（如果不存在）"""
        try:
            data = {"name": self.model}
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=data,
                timeout=300  # 5分钟超时，拉取模型可能需要时间
            )
            return response.status_code == 200
        except:
            return False 