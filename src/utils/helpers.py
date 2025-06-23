"""
辅助工具函数
"""

import os
import json
import yaml
from typing import Dict, Any, List
from datetime import datetime

def ensure_directory_exists(path: str) -> None:
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)

def save_json(data: Any, filepath: str) -> None:
    """保存JSON文件"""
    ensure_directory_exists(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath: str) -> Any:
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_yaml(data: Any, filepath: str) -> None:
    """保存YAML文件"""
    ensure_directory_exists(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

def load_yaml(filepath: str) -> Any:
    """加载YAML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def format_test_case_filename(feature_name: str, format_type: str = "md") -> str:
    """格式化测试用例文件名"""
    timestamp = get_timestamp()
    safe_name = "".join(c for c in feature_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')[:20]  # 限制长度
    return f"test_cases_{safe_name}_{timestamp}.{format_type}"

def format_test_data_filename(data_type: str, count: int, format_type: str = "json") -> str:
    """格式化测试数据文件名"""
    timestamp = get_timestamp()
    return f"test_data_{data_type}_{count}_{timestamp}.{format_type}"

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """验证文件扩展名"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions

def clean_text(text: str) -> str:
    """清理文本，移除多余的空白字符"""
    return ' '.join(text.split())

def truncate_text(text: str, max_length: int = 100) -> str:
    """截断文本到指定长度"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..." 