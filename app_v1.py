import streamlit as st
import tempfile
import os
from core.parser import PDFParser
from core.chunker import TextChunker
from core.embedder import LocalEmbedder
from core.graph_builder import GraphBuilder
from core.visualizer import GraphVisualizer
from utils.ollama_client import OllamaClient
import streamlit.components.v1 as components

# 页面配置
st.set_page_config(
    page_title="LocalScholar - 本地论文精读助手",
    page_icon="📚",
    layout="wide"
)

st.title("📚 LocalScholar")
st.caption("纯本地论文精读助手 · 数据不出电脑")

# 初始化
if "embedder" not in st.session_state:
    st.session_state.embedder = LocalEmbedder()
if "parser" not in st.session_state:
    st.session_state.parser = PDFParser()
if "chunker" not in st.session_state:
    st.session_state.chunker = TextChunker(chunk_size=500, chunk_overlap=50)
if "graph_builder" not in st.session_state:
    st.session_state.graph_builder = GraphBuilder()
if "visualizer" not in st.session_state:
    st.session_state.visualizer = GraphVisualizer()
if "ollama" not in st.session_state:
    st.session_state.ollama = OllamaClient("qwen2.5:7b")
if "ready" not in st.session_state:
    st.session_state.ready = False
if "graph_html" not in st.session_state:
    st.session_state.graph_html = None

# 侧边栏
with st.sidebar:
    st.header("📤 上传论文")
    uploaded_file = st.file_uploader(
        "选择PDF文件",
        type=["pdf"],
        help="支持学术论文、书籍PDF"
    )
    
    if uploaded_file:
        with st.spinner("正在处理论文..."):
            # 保存临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            # 1. 解析PDF
            result = st.session_state.parser.parse(tmp_path)
            st.success(f"✅ 解析完成！共 {result['metadata']['pages']} 页")
            
            # 2. 分块
            chunks = st.session_state.chunker.chunk_text(result["text"])
            st.success(f"✅ 分成 {len(chunks)} 个文本块")
            
            # 3. 向量化
            st.session_state.embedder.build_index(chunks)
            st.session_state.chunks = chunks
            st.success("✅ 向量索引构建完成")
            
            # 4. 构建知识图谱
            with st.spinner("正在构建知识图谱..."):
                graph = st.session_state.graph_builder.build_graph(result["text"])
                # 生成可视化HTML
                html_path = st.session_state.visualizer.visualize(
                    graph["entities"], 
                    graph["relations"],
                    "data/graph.html"
                )
                with open(html_path, "r", encoding="utf-8") as f:
                    st.session_state.graph_html = f.read()
                st.session_state.graph_data = graph
                st.success(f"✅ 知识图谱构建完成！{graph['stats']['entity_count']}个实体，{graph['stats']['relation_count']}条关系")
            
            st.session_state.ready = True
            os.unlink(tmp_path)

# 主区域 - 三列布局
tab1, tab2, tab3 = st.tabs(["📄 论文信息", "🕸️ 知识图谱", "💬 智能问答"])

with tab1:
    if st.session_state.ready:
        meta = st.session_state.parser.metadata
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**标题**: {meta.get('title', '未知')}")
            st.write(f"**作者**: {meta.get('author', '未知')}")
        with col2:
            st.write(f"**页数**: {meta.get('pages', 0)}")
            st.write(f"**文本块数**: {len(st.session_state.chunks)}")
        
        with st.expander("📑 章节预览"):
            sections = st.session_state.parser._extract_sections(st.session_state.parser.full_text)
            for section in sections[:10]:
                st.write(f"- {section['title']}")
    else:
        st.info("👈 请先上传PDF文件")

with tab2:
    if st.session_state.ready and st.session_state.graph_html:
        # 嵌入知识图谱HTML
        components.html(st.session_state.graph_html, height=700, scrolling=True)
        
        # 统计信息
        if "graph_data" in st.session_state:
            stats = st.session_state.graph_data["stats"]
            st.write(f"📊 共 {stats['entity_count']} 个实体，{stats['relation_count']} 条关系")
            st.write("**实体类型分布**:", stats["entity_types"])
    else:
        st.info("👈 请先上传PDF文件")

with tab3:
    if st.session_state.ready:
        query = st.text_input("💬 输入你的问题", placeholder="例如：这篇论文主要解决了什么问题？")
        if query and st.button("🔍 提问", type="primary"):
            with st.spinner("正在检索和生成答案..."):
                # 1. 检索相关段落
                results = st.session_state.embedder.search(query, top_k=5)
                
                # 2. 拼接上下文
                context = "\n---\n".join([chunk["text"] for chunk, score in results[:4]])
                
                # 3. 调用本地模型
                answer = st.session_state.ollama.generate_answer(context, query)
                
                # 4. 显示结果
                st.markdown("### 🤖 答案")
                st.markdown(answer)
                
                # 5. 显示参考段落
                with st.expander("📎 参考段落 (点击展开)"):
                    for chunk, score in results:
                        st.write(f"**相关度 {score:.3f}**")
                        st.write(chunk["text"])
                        st.divider()
    else:
        st.info("👈 请先上传PDF文件")

# 底部
st.divider()
st.caption("🔒 所有处理均在本地完成，数据不会上传到任何服务器 · 使用 Ollama + Qwen2.5")