"""
项目配置管理
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Settings(BaseSettings):
    """项目配置"""
    
    # LLaMA模型配置 (使用Ollama)
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llama_model: str = os.getenv("LLAMA_MODEL", "llama2:7b-chat")
    model_temperature: float = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2000"))
    
    # 项目配置
    project_name: str = os.getenv("PROJECT_NAME", "AI测试用例生成器")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Web配置
    web_port: int = int(os.getenv("WEB_PORT", "8501"))
    web_host: str = os.getenv("WEB_HOST", "localhost")
    
    # 数据配置
    default_locale: str = os.getenv("DEFAULT_LOCALE", "zh_CN")
    default_test_framework: str = os.getenv("DEFAULT_TEST_FRAMEWORK", "pytest")
    
    # Google API Key
    google_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_ollama_connection(self) -> bool:
        """验证Ollama服务是否可用"""
        try:
            import requests
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_model_config(self) -> dict:
        """获取模型配置"""
        return {
            "model": self.llama_model,
            "temperature": self.model_temperature,
            "max_tokens": self.max_tokens,
            "base_url": self.ollama_base_url
        }

    def validate_api_key(self) -> bool:
        """检查Google API密钥是否存在"""
        return self.google_api_key is not None and self.google_api_key != "YOUR_GOOGLE_API_KEY" 