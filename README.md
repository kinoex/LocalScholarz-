# LocalScholarz-
一个叫 GraphRAG 的技术正在成为新趋势。它用知识图谱把文献之间的关系结构化，能捕捉普通RAG（检索增强生成）看不出来的“远距离隐藏信息”，生成更全面、直观的图谱式摘要。像Academic Cluster项目，就已经集成了知识图谱抽取功能，本工具旨在Ai读文，省去部分时间，方便大家看书
本工具部署在本地主打隐私优先的“精读+图谱”工具
✨ 核心功能 
上传 PDF 自动解析（标题/作者/章节） 
智能分块 + 向量检索，秒级定位相关段落 
自动生成知识图谱，可视化展示论文核心概念和关系 
接入 Ollama 本地模型，基于论文内容深度问答 
全部本地运行，数据不上传.
技术栈 Streamlit + pdfplumber + Sentence-Transformers + FAISS + pyvis + Ollama
Here's the English translation:
A technology called GraphRAG is emerging as a new trend. It uses knowledge graphs to structure the relationships between documents, capturing "long-range hidden information" that ordinary RAG (Retrieval-Augmented Generation) fails to detect, and producing more comprehensive, intuitive graph-based summaries. Projects like Academic Cluster have already integrated knowledge graph extraction capabilities. This tool is designed for AI-powered document reading, saving time and making it easier for everyone to read papers.
This is a privacy-first "deep reading + graph" tool deployed locally.
✨ Core Features
📄 Upload PDFs for automatic parsing (title, author, sections)
🧠 Intelligent chunking + vector retrieval — locate relevant paragraphs in seconds
🕸️ Auto-generate knowledge graphs — visualize core concepts and their relationships
💬 Integrate with Ollama local models for in-depth Q&A based on paper content
🔒 Fully local execution — data never leaves your machine
🛠️ Tech Stack
Streamlit + pdfplumber + Sentence-Transformers + FAISS + pyvis + Ollama
