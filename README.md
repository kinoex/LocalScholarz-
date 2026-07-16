# 📚 LocalScholar

[![Python Version](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/local-scholar)](https://github.com/yourusername/local-scholar)

> 🔒 **本地部署 Local Deployment** · 🕸️ **知识图谱 Knowledge Graph** · 💬 **智能问答 Intelligent Q&A**
> 让AI帮你精读论文，数据永远留在你的电脑里。
> Let AI help you read papers deeply — your data never leaves your computer.

---

## ✨ 核心功能一览 / Core Features

- 📄 **智能PDF解析 Smart PDF Parsing**：自动提取标题、作者、章节结构，论文概览一目了然。Automatically extracts title, author, and section structure for an instant paper overview.
- 🧠 **语义分块与检索 Semantic Chunking & Retrieval**：基于语义切割长文本，配合本地向量模型，秒级定位关键段落。Splits long texts semantically and pairs with a local embedding model to locate key paragraphs in seconds.
- 🕸️ **自动知识图谱 Auto Knowledge Graph**：**这是本项目的核心亮点！This is the core highlight!** 自动抽取论文中的核心概念与关系，生成交互式图谱，帮你直观理解复杂结构。Automatically extracts core concepts and relationships from papers, generating an interactive graph for intuitive understanding of complex structures.
- 💬 **本地大模型问答 Local LLM Q&A**：集成 Ollama，让你基于论文内容进行深度提问，全程离线，无需担心数据外泄。Integrates Ollama for deep, context-aware questioning based on paper content — fully offline, zero data leakage.
- 🔒 **百分百隐私安全 100% Privacy-First**：所有处理流程均在本地完成，**绝不向任何服务器上传数据**。All processing happens locally on your machine. **Absolutely no data is uploaded to any server.**

## 🎯 这适合谁用？/ Who Is This For?

*   🧑‍🔬 **科研人员与研究生 Researchers & Grad Students**：快速梳理文献脉络，抓住研究重点。Quickly map out literature and grasp research highlights.
*   🎓 **学生与自学者 Students & Self-Learners**：深入理解复杂学术概念，辅助课程学习。Deeply understand complex academic concepts and support coursework.
*   🧑‍💼 **知识工作者 Knowledge Workers**：构建个人本地知识库，高效处理信息。Build a personal local knowledge base and process information efficiently.
*   🔐 **隐私敏感用户 Privacy-Conscious Users**：处理未发表或机密文档时，彻底杜绝泄露风险。Handle unpublished or confidential documents with zero leakage risk.

## 🚀 五分钟快速上手 / Quick Start (5 Minutes)

### 前置准备 / Prerequisites
*   Python 3.8+
*   [Ollama](https://ollama.com/) (用于运行本地模型 / for running local models)

### 安装与启动 / Install & Launch
```bash
# 1. 克隆项目 / Clone the repo
git clone https://github.com/kinoex/LocalScholarz-.git
cd local-scholar

# 2. 安装Python依赖 / Install Python dependencies
pip install -r requirements.txt

# 3. 拉取并运行本地模型 / Pull a local model (Qwen2.5 as example)
ollama pull qwen2.5:7b

# 4. 启动应用 / Launch the app
streamlit run app_v1.py
```
启动后，浏览器会自动打开 `http://localhost:8501`，开始你的首次精读体验。
Once started, your browser will open `http://localhost:8501` automatically. Enjoy your first deep-reading session!

## 📖 如何使用 / How to Use

1. **上传论文 Upload a Paper**：在左侧栏上传你的PDF文件。Drop your PDF in the left sidebar.
2. **自动处理 Auto-Processing**：系统将依次完成 解析 → 分块 → 向量化 → 知识图谱构建。The system will sequentially complete parsing → chunking → embedding → knowledge graph construction.
3. **探索与问答 Explore & Ask**：
   - 在 **"知识图谱 Knowledge Graph"** 标签页，拖动和点击节点，探索概念间的关联。Drag and click nodes to explore concept relationships.
   - 在 **"智能问答 Intelligent Q&A"** 标签页，输入任何问题，AI将基于论文内容为你解答。Type any question and the AI will answer based on the paper content.

## 🛠️ 技术实现 / Tech Stack

| 功能组件 Component | 采用技术 Technology | 作用 Purpose |
|-------------------|-------------------|-------------|
| 前端界面 Frontend | Streamlit | 快速构建交互式Web应用 / Rapidly build interactive web apps |
| PDF解析 PDF Parsing | pdfplumber | 精准提取PDF文本与元数据 / Precisely extract PDF text and metadata |
| 文本处理 Text Processing | LangChain | 智能文本分块，保留语义 / Intelligent semantic text chunking |
| 向量引擎 Vector Engine | Sentence-Transformers & FAISS | 本地文本嵌入与高效相似度检索 / Local text embedding and efficient similarity search |
| 知识图谱 Knowledge Graph | pyvis | 生成并可视化交互式知识图谱 / Generate and visualize interactive knowledge graphs |
| 本地模型 Local LLM | Ollama + Qwen2.5 | 提供高质量的离线智能问答 / High-quality offline intelligent Q&A |

## 📁 项目结构 / Project Structure

```
local-scholar/
├── core/               # 核心功能模块 / Core modules
│   ├── parser.py       # PDF解析 / PDF parsing
│   ├── chunker.py      # 文本分块 / Text chunking
│   ├── embedder.py     # 向量嵌入与检索 / Vector embedding & retrieval
│   ├── graph_builder.py # 知识图谱构建 / Knowledge graph construction
│   └── visualizer.py   # 图谱可视化 / Graph visualization
├── utils/              # 辅助工具 / Utilities
│   ├── ollama_client.py # Ollama API封装 / Ollama API wrapper
│   └── cache.py        # 缓存管理器 / Cache manager
├── tests/              # 单元测试 / Unit tests
├── scripts/            # 构建与辅助脚本 / Build & helper scripts
├── app_v1.py           # 应用主入口 / Main app entry
├── requirements.txt    # 项目依赖 / Dependencies
└── README.md           # 项目说明 / This file
```

## 🤝 参与贡献 / Contributing

我们欢迎任何形式的贡献！无论是报告Bug、提出新功能，还是提交代码，都请先查看贡献指南。
We welcome all forms of contribution! Whether reporting bugs, proposing new features, or submitting code, please check the contribution guidelines first.

## 📄 许可证 / License

本项目采用 MIT 许可证，意味着你可以自由使用、修改、分发，甚至用于商业项目。详情请见 [LICENSE](LICENSE) 文件。
This project is licensed under the MIT License, meaning you are free to use, modify, distribute, and even use it commercially. See the [LICENSE](LICENSE) file for details.

如果这个项目对你有帮助，请点个 ⭐ 支持一下，让它能帮到更多人！
If this project helps you, please give it a ⭐ so it can help more people!
