"""
测试用例生成器 - 根据功能描述生成详细的测试用例
"""

import json
import yaml
from typing import Dict, List, Optional
from ..config.settings import Settings
from ..utils.llama_client import LlamaClient

class TestCaseGenerator:
    """测试用例生成器"""
    
    def __init__(self):
        self.settings = Settings()
        # 配置LLaMA客户端
        self.llama_client = LlamaClient()
        
    def generate_from_description(self, feature_description: str, test_framework: str = "pytest") -> str:
        """根据功能描述生成测试用例"""
        
        system_prompt = f"""你是一个专业的测试工程师，需要根据功能描述生成详细的测试用例。

请按照以下格式生成测试用例：

## 功能：{{功能名称}}

### 正向测试用例
1. **测试用例名**: xxx
   - **前置条件**: xxx
   - **测试步骤**: 
     1. xxx
     2. xxx
   - **预期结果**: xxx
   - **优先级**: 高/中/低

### 负向测试用例
1. **测试用例名**: xxx
   - **前置条件**: xxx
   - **测试步骤**: 
     1. xxx
     2. xxx
   - **预期结果**: xxx
   - **优先级**: 高/中/低

### 边界测试用例
1. **测试用例名**: xxx
   - **前置条件**: xxx
   - **测试步骤**: 
     1. xxx
     2. xxx
   - **预期结果**: xxx
   - **优先级**: 高/中/低

请确保：
1. 覆盖正常流程、异常流程和边界情况
2. 测试步骤清晰具体
3. 预期结果明确可验证
4. 优先级设置合理

测试框架：{test_framework}
"""
        
        try:
            # 使用LLaMA生成响应
            prompt = f"请为以下功能生成测试用例：{feature_description}"
            response = self.llama_client.generate_content(prompt, system_prompt)
            return response
            
        except Exception as e:
            return f"生成测试用例时出现错误：{str(e)}"
    
    def generate_from_features(self, features_text: str, output_format: str = "json") -> str:
        """从功能列表生成批量测试用例"""
        try:
            # 分割功能描述
            features = [f.strip() for f in features_text.split('\n') if f.strip()]
            
            all_test_cases = []
            
            for feature in features:
                test_case = self.generate_from_description(feature)
                all_test_cases.append({
                    'feature': feature,
                    'test_cases': test_case
                })
            
            # 根据格式返回结果
            if output_format == "json":
                return json.dumps(all_test_cases, ensure_ascii=False, indent=2)
            elif output_format == "yaml":
                return yaml.dump(all_test_cases, allow_unicode=True, default_flow_style=False)
            else:
                # 纯文本格式
                text_output = ""
                for i, tc in enumerate(all_test_cases, 1):
                    text_output += f"\n{'='*50}\n功能 {i}: {tc['feature']}\n{'='*50}\n"
                    text_output += tc['test_cases'] + "\n"
                return text_output
                
        except Exception as e:
            return f"批量生成测试用例时出现错误：{str(e)}"
    
    def generate_api_test_cases(self, api_spec: Dict) -> str:
        """根据API规范生成测试用例"""
        
        system_prompt = """你是一个API测试专家，需要根据API规范生成详细的测试用例。

请生成以下类型的测试用例：
1. 正常请求测试
2. 参数验证测试
3. 权限验证测试
4. 错误处理测试
5. 性能测试考虑

每个测试用例包含：
- 请求方法和URL
- 请求参数/Body
- 预期状态码
- 预期响应格式
- 测试目的
"""
        
        try:
            # 使用LLaMA生成响应
            prompt = f"请为以下API生成测试用例：{json.dumps(api_spec, ensure_ascii=False, indent=2)}"
            response = self.llama_client.generate_content(prompt, system_prompt)
            return response
            
        except Exception as e:
            return f"生成API测试用例时出现错误：{str(e)}"
    
    def generate_automation_code(self, test_cases: str, framework: str = "pytest") -> str:
        """将测试用例转换为自动化测试代码"""
        
        system_prompt = f"""你是一个测试自动化专家，需要将测试用例转换为可执行的自动化测试代码。

使用测试框架：{framework}

请生成：
1. 完整的测试类和方法
2. 必要的setup和teardown
3. 断言和验证逻辑
4. 适当的注释和文档

代码应该：
- 遵循最佳实践
- 易于维护和扩展
- 包含错误处理
- 具有良好的可读性
"""
        
        try:
            # 使用LLaMA生成响应
            prompt = f"请将以下测试用例转换为自动化测试代码：\n{test_cases}"
            response = self.llama_client.generate_content(prompt, system_prompt)
            return response
            
        except Exception as e:
            return f"生成自动化测试代码时出现错误：{str(e)}" 