#!/usr/bin/env python3
"""
LLaMA集成测试脚本
用于验证LLaMA模型是否正确集成到项目中
"""

import sys
from src.utils.llama_client import LlamaClient
from src.config.settings import Settings
from src.agents.test_agent import TestAgent
from src.generators.test_case_generator import TestCaseGenerator

def test_ollama_connection():
    """测试Ollama连接"""
    print("🔍 测试Ollama连接...")
    settings = Settings()
    
    if settings.validate_ollama_connection():
        print("✅ Ollama服务连接成功")
        return True
    else:
        print("❌ Ollama服务连接失败")
        print(f"请确保Ollama服务在 {settings.ollama_base_url} 运行")
        return False

def test_model_availability():
    """测试模型可用性"""
    print("🔍 测试模型可用性...")
    client = LlamaClient()
    
    if client.check_model_availability():
        print(f"✅ 模型 {client.model} 可用")
        return True
    else:
        print(f"❌ 模型 {client.model} 不可用")
        print(f"请运行: ollama pull {client.model}")
        return False

def test_llama_client():
    """测试LLaMA客户端"""
    print("🔍 测试LLaMA客户端...")
    client = LlamaClient()
    
    try:
        response = client.generate_content("你好，请简单介绍一下自己")
        if response and "错误" not in response:
            print("✅ LLaMA客户端工作正常")
            print(f"响应示例: {response[:100]}...")
            return True
        else:
            print("❌ LLaMA客户端响应异常")
            print(f"响应: {response}")
            return False
    except Exception as e:
        print(f"❌ LLaMA客户端测试失败: {e}")
        return False

def test_test_case_generator():
    """测试测试用例生成器"""
    print("🔍 测试测试用例生成器...")
    generator = TestCaseGenerator()
    
    try:
        result = generator.generate_from_description("用户登录功能", "pytest")
        if result and "错误" not in result:
            print("✅ 测试用例生成器工作正常")
            print(f"生成示例: {result[:100]}...")
            return True
        else:
            print("❌ 测试用例生成器异常")
            print(f"结果: {result}")
            return False
    except Exception as e:
        print(f"❌ 测试用例生成器测试失败: {e}")
        return False

def test_test_agent():
    """测试测试代理"""
    print("🔍 测试测试代理...")
    agent = TestAgent()
    
    try:
        response = agent.chat("你好，请介绍一下你的功能")
        if response and "错误" not in response:
            print("✅ 测试代理工作正常")
            print(f"响应示例: {response[:100]}...")
            return True
        else:
            print("❌ 测试代理响应异常")
            print(f"响应: {response}")
            return False
    except Exception as e:
        print(f"❌ 测试代理测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始LLaMA集成测试...\n")
    
    tests = [
        ("Ollama连接", test_ollama_connection),
        ("模型可用性", test_model_availability),
        ("LLaMA客户端", test_llama_client),
        ("测试用例生成器", test_test_case_generator),
        ("测试代理", test_test_agent)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- 测试: {test_name} ---")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！LLaMA集成成功！")
        print("\n💡 现在可以使用以下命令启动项目:")
        print("   python main.py chat -i    # 启动对话模式")
        print("   python main.py web        # 启动Web界面")
    else:
        print("⚠️ 部分测试失败，请检查配置和环境")
        print("\n🔧 故障排除:")
        print("1. 确保Ollama服务正在运行: ollama serve")
        print("2. 确保模型已下载: ollama pull llama2:7b-chat")
        print("3. 检查config.env配置文件")
        sys.exit(1)

if __name__ == "__main__":
    main() 