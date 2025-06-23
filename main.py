#!/usr/bin/env python3
"""
AI测试用例生成器 - 主程序入口
支持命令行、Web界面和API多种使用方式
"""

import click
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# 加载环境变量
load_dotenv()

console = Console()

@click.group()
def cli():
    """AI测试用例生成器 - 智能测试助手"""
    pass

@cli.command()
@click.option('--interactive', '-i', is_flag=True, help='启用交互式对话模式')
def chat(interactive):
    """启动对话模式"""
    from src.agents.test_agent import TestAgent
    
    console.print(Panel("🤖 AI测试用例生成器启动", style="bold green"))
    
    agent = TestAgent()
    
    if interactive:
        console.print("输入 'quit' 或 'exit' 退出程序\n")
        
        while True:
            try:
                user_input = console.input("[bold blue]您: [/bold blue]")
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    console.print("👋 再见！")
                    break
                
                response = agent.chat(user_input)
                console.print(f"[bold green]AI助手: [/bold green]{response}")
                
            except KeyboardInterrupt:
                console.print("\n👋 再见！")
                break
            except Exception as e:
                console.print(f"[red]错误: {e}[/red]")

@cli.command()
@click.option('--input', '-i', required=True, help='输入的功能描述文件')
@click.option('--output', '-o', default='./output', help='输出目录')
@click.option('--format', '-f', default='json', help='输出格式 (json/yaml/txt)')
def generate(input, output, format):
    """批量生成测试用例"""
    from src.generators.test_case_generator import TestCaseGenerator
    
    console.print(f"🔄 正在处理文件: {input}")
    
    generator = TestCaseGenerator()
    
    # 确保输出目录存在
    os.makedirs(output, exist_ok=True)
    
    try:
        with open(input, 'r', encoding='utf-8') as f:
            features = f.read()
        
        test_cases = generator.generate_from_features(features, format)
        
        output_file = os.path.join(output, f'test_cases.{format}')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(test_cases)
        
        console.print(f"✅ 测试用例已生成到: {output_file}")
        
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")

@cli.command()
@click.option('--port', '-p', default=8501, help='Web服务端口')
@click.option('--host', '-h', default='localhost', help='Web服务地址')
def web(port, host):
    """启动Web界面"""
    console.print(f"🌐 启动Web界面: http://{host}:{port}")
    
    try:
        import subprocess
        subprocess.run(['streamlit', 'run', 'src/web/app.py', '--server.port', str(port), '--server.address', host])
    except Exception as e:
        console.print(f"[red]启动Web界面失败: {e}[/red]")
        console.print("请确保已安装streamlit: pip install streamlit")

@cli.command()
@click.option('--type', '-t', default='user', help='数据类型 (user/product/order等)')
@click.option('--count', '-c', default=10, help='生成数量')
@click.option('--output', '-o', default='./test_data.json', help='输出文件')
def data(type, count, output):
    """生成测试数据"""
    from src.generators.data_generator import DataGenerator
    
    console.print(f"🔧 正在生成 {count} 条 {type} 类型的测试数据...")
    
    generator = DataGenerator()
    test_data = generator.generate_data(type, count)
    
    import json
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    console.print(f"✅ 测试数据已生成到: {output}")

if __name__ == '__main__':
    cli() 