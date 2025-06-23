# Agentic AI RAG 测试平台

一个基于 RAG (Retrieval-Augmented Generation) 架构的 Agentic AI 测试平台，旨在提供一个本地、可控的环境，用于测试和调试 AI Agent 的知识获取与决策能力。

该平台集成了 Streamlit 可视化界面、基于本地大语言模型（通过 Ollama）的 Agent 以及一个由本地文档构建的知识库。

## ✨ 功能特性

- 🧠 **RAG 集成**：Agent 的回答由其从本地知识库中检索到的信息增强，模拟真实世界中的知识密集型任务。
- 🔍 **可视化调试面板**：在聊天界面中，清晰地展示用户输入、检索到的上下文以及 Agent 的最终输出，便于分析和调试。
- 🏠 **完全本地化**：使用 Ollama 在本地运行 Llama 3 等大语言模型，确保数据隐私和安全。
- 🔧 **动态知识库**：基于本地文件（例如 `examples/sample_features.txt`）构建向量知识库，易于扩展和定制。
- 💬 **交互式 Agent 界面**：通过 Streamlit 提供友好的聊天界面，与 AI Agent 进行实时交互。

## 🏛️ 系统架构

```
+--------------------------------+
|  Streamlit Web UI              |
|  (Chat, Context Visualization) |
+----------------+---------------+
                 |
                 v
+----------------+---------------+
|  TestAgent                     |  ← 核心 Agent 逻辑
+----------------+---------------+
                 |
                 v
+----------------+---------------+
|  RAG Module (Retriever)        |  ← FAISS 向量知识库
+----------------+---------------+
                 |
                 v
+--------------------------------+
|  Ollama (LLM Backend)          |  ← 本地运行 Llama 3
+--------------------------------+
```

## 🚀 快速开始

### 1. 准备环境：Ollama 和大语言模型

确保您已在本地安装了 Ollama，并拉取了所需的语言模型。

```bash
# 访问 ollama.com 安装 Ollama

# 拉取 Llama 3 模型
ollama pull llama3
```
*该项目默认使用 `llama3`，您可以在 `src/config/settings.py` 中修改配置。*

### 2. 设置项目

克隆项目后，创建虚拟环境并安装依赖。

```bash
# 创建并激活 Python 虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装项目依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

项目需要一个环境变量文件来配置 Ollama 和其他设置。

复制 `config.env.example`（如果存在）或手动创建一个名为 `config.env` 的文件，并填入以下内容：

```env
# Ollama 配置
OLLAMA_BASE_URL=http://localhost:11434
LLAMA_MODEL=llama3

# Google API Key (当前 Web UI 启动时需要)
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```
> **注意**: 即使我们主要依赖本地的 Ollama，`src/web/app.py` 中保留了对 `GOOGLE_API_KEY` 的检查。您可以暂时填入一个任意字符串以通过检查。

### 4. 运行应用

完成以上步骤后，使用 Streamlit 启动 Web 应用。

```bash
streamlit run src/web/app.py
```

应用启动后，浏览器将自动打开 Web 界面。

## 💡 使用方法

1.  打开 Web 界面后，从侧边栏选择 **"💬 智能对话"** 模式。
2.  在底部的聊天框中输入您的问题，例如："用户登录功能应该如何测试？"
3.  Agent 会作出回答。如果回答是基于知识库的，您会看到一个可展开的 **"🔍 查看检索上下文"** 区域，其中包含了 Agent 用来生成答案的原始信息。
4.  您可以通过查看上下文来评估 Agent 的检索准确性和回答质量。

## 项目结构

```
ai-test-generator/
├── src/
│   ├── agents/             # AI代理核心逻辑
│   ├── generators/         # 测试用例和数据生成器
│   ├── templates/          # 测试用例模板
│   ├── utils/              # 工具函数
│   └── config/             # 配置文件
├── examples/               # 示例和演示
├── tests/                  # 项目测试
└── docs/                   # 文档
```

## 📖 详细使用指南

请参阅 [LLaMA模型安装和配置指南](README_LLAMA_SETUP.md) 了解如何安装和配置LLaMA模型。

## 🔧 系统要求

- Python 3.8+
- 至少8GB RAM（用于运行LLaMA 2 7B模型）
- 4GB可用磁盘空间（用于存储模型） 