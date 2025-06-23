# LLaMA模型安装和配置指南

本项目已更新为使用Meta的LLaMA模型，通过Ollama运行。以下是详细的安装和配置步骤。

## 安装Ollama

### Windows
1. 访问 [Ollama官网](https://ollama.ai/)
2. 下载Windows安装包
3. 运行安装程序并按照提示完成安装

### macOS
```bash
# 使用Homebrew安装
brew install ollama

# 或者从官网下载安装包
curl -fsSL https://ollama.ai/install.sh | sh
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## 启动Ollama服务

安装完成后，启动Ollama服务：

```bash
ollama serve
```

服务将在 `http://localhost:11434` 运行。

## 下载LLaMA模型

使用以下命令下载推荐的LLaMA模型：

```bash
# 下载LLaMA 2 7B Chat模型（推荐，较小但足够强大）
ollama pull llama2:7b-chat

# 或者下载更大的模型（需要更多内存）
ollama pull llama2:13b-chat
ollama pull llama2:70b-chat

# 也可以使用CodeLlama模型（专为代码生成优化）
ollama pull codellama:7b-instruct
```

## 配置项目

1. 确保 `config.env` 文件中的配置正确：
```env
# LLaMA模型配置 (使用Ollama)
OLLAMA_BASE_URL=http://localhost:11434
LLAMA_MODEL=llama2:7b-chat
MODEL_TEMPERATURE=0.7
```

2. 如果使用不同的模型，请修改 `LLAMA_MODEL` 参数：
   - `llama2:7b-chat` - 7B参数模型，速度快，内存需求较低
   - `llama2:13b-chat` - 13B参数模型，更准确，需要更多内存
   - `codellama:7b-instruct` - 专为代码生成优化的模型

## 验证安装

运行以下命令验证模型是否正确安装：

```bash
# 列出已安装的模型
ollama list

# 测试模型
ollama run llama2:7b-chat "你好，请介绍一下自己"
```

## 系统要求

- **内存要求**：
  - 7B模型：至少8GB RAM
  - 13B模型：至少16GB RAM
  - 70B模型：至少64GB RAM

- **存储空间**：
  - 7B模型：约4GB
  - 13B模型：约7GB
  - 70B模型：约39GB

## 运行项目

确保Ollama服务运行并且模型已下载后，可以正常使用项目：

```bash
# 安装依赖
pip install -r requirements.txt

# 启动对话模式
python main.py chat -i

# 启动Web界面
python main.py web
```

## 常见问题

### Q: Ollama服务无法启动
A: 检查端口11434是否被占用，可以使用 `netstat -an | grep 11434` 查看

### Q: 模型下载速度慢
A: 可以尝试使用国内镜像或者在网络较好的环境下下载

### Q: 内存不足
A: 尝试使用较小的模型，如 `llama2:7b-chat` 而不是更大的模型

### Q: 生成速度慢
A: 考虑使用GPU版本的Ollama，或者使用更强的硬件

## 模型选择建议

- **开发和测试**：使用 `llama2:7b-chat`
- **生产环境**：根据准确性需求选择 `llama2:13b-chat` 或 `llama2:70b-chat`
- **代码生成**：使用 `codellama:7b-instruct` 或 `codellama:13b-instruct`

## 技术支持

如果遇到问题，请：
1. 查看Ollama官方文档：https://ollama.ai/
2. 检查项目的GitHub Issues
3. 确保Ollama服务正常运行并且模型已正确下载 