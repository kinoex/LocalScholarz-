import pytest
from core.chunker import TextChunker

def test_chunk_text():
    """测试文本分块"""
    chunker = TextChunker(chunk_size=100, chunk_overlap=10)
    text = "这是一段测试文本。" * 20
    chunks = chunker.chunk_text(text)
    assert len(chunks) > 0
    assert all("id" in c and "text" in c for c in chunks)
