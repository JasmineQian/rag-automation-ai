#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    print(f"✅ Python版本: {sys.version}")

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        sys.exit(1)

def setup_environment():
    """设置环境变量"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚙️ 创建环境配置文件...")
        
        # 复制配置模板
        config_template = Path("config.env")
        if config_template.exists():
            with open(config_template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 环境配置文件已创建: .env")
            print("🔑 请编辑 .env 文件，添加您的Google API密钥")
        else:
            print("❌ 配置模板文件不存在")
    else:
        print("✅ 环境配置文件已存在")

def create_directories():
    """创建必要的目录"""
    directories = ['output', 'logs', 'examples']
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 创建目录: {dir_name}")

def main():
    """主安装流程"""
    print("🚀 AI测试用例生成器 - 安装向导")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 安装依赖
    install_dependencies()
    
    # 设置环境
    setup_environment()
    
    # 创建目录
    create_directories()
    
    print("\n" + "=" * 50)
    print("🎉 安装完成!")
    print("\n📖 下一步:")
    print("1. 编辑 .env 文件，添加您的Google API密钥")
    print("2. 运行命令测试:")
    print("   python main.py chat --interactive")
    print("3. 启动Web界面:")
    print("   python main.py web")
    print("\n💡 更多帮助: python main.py --help")

if __name__ == "__main__":
    main() 