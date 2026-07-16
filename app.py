import streamlit as st
import tempfile
import os
from core.parser import PDFParser
from core.chunker import TextChunker
from core.embedder import LocalEmbedder

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
if "ready" not in st.session_state:
    st.session_state.ready = False

# 侧边栏
with st.sidebar:
    st.header("📤 上传论文")
    uploaded_file = st.file_uploader(
        "选择PDF文件",
        type=["pdf"],
        help="支持学术论文、书籍PDF"
    )
    
    if uploaded_file:
        with st.spinner("正在解析PDF..."):
            # 保存临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            # 解析
            result = st.session_state.parser.parse(tmp_path)
            st.success(f"✅ 解析完成！共 {result['metadata']['pages']} 页")
            
            # 分块
            with st.spinner("正在分块..."):
                chunks = st.session_state.chunker.chunk_text(result["text"])
                st.success(f"✅ 分成 {len(chunks)} 个文本块")
            
            # 向量化
            with st.spinner("正在构建向量索引（首次需下载模型）..."):
                st.session_state.embedder.build_index(chunks)
                st.session_state.chunks = chunks
                st.session_state.ready = True
                st.success("✅ 索引构建完成！可以开始提问了")
            
            # 清理临时文件
            os.unlink(tmp_path)

# 主区域
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 论文信息")
    if "ready" in st.session_state and st.session_state.ready:
        meta = st.session_state.parser.metadata
        st.write(f"**标题**: {meta.get('title', '未知')}")
        st.write(f"**作者**: {meta.get('author', '未知')}")
        st.write(f"**页数**: {meta.get('pages', 0)}")
        
        # 显示章节预览
        with st.expander("📑 章节预览"):
            for section in st.session_state.parser._extract_sections(st.session_state.parser.full_text)[:5]:
                st.write(f"- {section['title']}")
    else:
        st.info("👈 请先上传PDF文件")

with col2:
    st.subheader("💬 问答")
    if st.session_state.ready:
        query = st.text_input("输入你的问题", placeholder="例如：这篇论文主要解决了什么问题？")
        if query and st.button("🔍 提问"):
            with st.spinner("正在检索和生成答案..."):
                results = st.session_state.embedder.search(query, top_k=5)
                
                st.write("**📎 相关段落：**")
                for chunk, score in results[:3]:
                    with st.expander(f"相关度 {score:.3f}"):
                        st.write(chunk["text"])
                
                # TODO: 接入本地大模型生成答案
                st.info("🤖 下一步将接入Ollama本地模型生成完整答案")
    else:
        st.info("👈 请先上传论文")

# 底部
st.divider()
st.caption("🔒 所有处理均在本地完成，数据不会上传到任何服务器")