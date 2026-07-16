
# 📚 LocalScholar

[![Python Version](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/local-scholar)](https://github.com/yourusername/local-scholar)

> 🔒 **本地部署** · 🕸️ **知识图谱** · 💬 **智能问答**
> 让AI帮你精读论文，数据永远留在你的电脑里。

---

## ✨ 核心功能一览

- 📄 **智能PDF解析**：自动提取标题、作者、章节结构，论文概览一目了然。
- 🧠 **语义分块与检索**：基于语义切割长文本，配合本地向量模型，秒级定位关键段落。
- 🕸️ **自动知识图谱**：**这是本项目的核心亮点！** 自动抽取论文中的核心概念与关系，生成交互式图谱，帮你直观理解复杂结构。
- 💬 **本地大模型问答**：集成 Ollama，让你基于论文内容进行深度提问，全程离线，无需担心数据外泄。
- 🔒 **百分百隐私安全**：所有处理流程均在本地完成，**绝不向任何服务器上传数据**。

## 🎯 这适合谁用？

*   🧑‍🔬 **科研人员与研究生**：快速梳理文献脉络，抓住研究重点。
*   🎓 **学生与自学者**：深入理解复杂学术概念，辅助课程学习。
*   🧑‍💼 **知识工作者**：构建个人本地知识库，高效处理信息。
*   🔐 **隐私敏感用户**：处理未发表或机密文档时，彻底杜绝泄露风险。

## 🚀 五分钟快速上手

### 前置准备
*   Python 3.8+
*   [Ollama](https://ollama.com/) (用于运行本地模型)

### 安装与启动
```bash
# 1. 克隆项目
git clone https://github.com/yourusername/local-scholar.git
cd local-scholar

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 拉取并运行本地模型 (以Qwen2.5为例)
ollama pull qwen2.5:7b

# 4. 启动应用
streamlit run app_v1.py
启动后，浏览器会自动打开 http://localhost:8501，开始你的首次精读体验。

📖 如何使用
上传论文：在左侧栏上传你的PDF文件。

自动处理：系统将依次完成 解析 → 分块 → 向量化 → 知识图谱构建。

探索与问答：

在 “知识图谱” 标签页，拖动和点击节点，探索概念间的关联。

在 “智能问答” 标签页，输入任何问题，AI将基于论文内容为你解答。

🛠️ 技术实现
功能组件	采用技术	作用
前端界面	Streamlit	快速构建交互式Web应用
PDF解析	pdfplumber	精准提取PDF文本与元数据
文本处理	LangChain	智能文本分块，保留语义
向量引擎	Sentence-Transformers & FAISS	本地文本嵌入与高效相似度检索
知识图谱	pyvis	生成并可视化交互式知识图谱
本地模型	Ollama + Qwen2.5	提供高质量的离线智能问答
📁 项目结构
text
local-scholar/
├── core/               # 核心功能模块
│   ├── parser.py       # PDF解析
│   ├── chunker.py      # 文本分块
│   ├── embedder.py     # 向量嵌入与检索
│   ├── graph_builder.py # 知识图谱构建
│   └── visualizer.py   # 图谱可视化
├── utils/              # 辅助工具
│   ├── ollama_client.py # Ollama API封装
│   └── cache.py        # 缓存管理器
├── tests/              # 单元测试
├── scripts/            # 构建与辅助脚本
├── app_v1.py           # 应用主入口
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明 (就是本文件)
🤝 参与贡献
我们欢迎任何形式的贡献！无论是报告Bug、提出新功能，还是提交代码，都请先查看 贡献指南。

📄 许可证
本项目采用 MIT 许可证，意味着你可以自由使用、修改、分发，甚至用于商业项目。详情请见 LICENSE 文件。

如果这个项目对你有帮助，请点个 ⭐ 支持一下，让它能帮到更多人！