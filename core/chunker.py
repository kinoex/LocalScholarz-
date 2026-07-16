from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import re

class TextChunker:
    """文本分块器：按语义将长文本切分成小块"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", "；", ",", " ", ""]
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[Dict]:
        """
        分块并返回带元数据的块列表
        每个块包含：id, text, start_char, end_char
        """
        chunks = self.splitter.split_text(text)
        
        result = []
        char_count = 0
        for i, chunk in enumerate(chunks):
            start = char_count
            end = char_count + len(chunk)
            char_count = end
            
            result.append({
                "id": f"chunk_{i:04d}",
                "text": chunk,
                "start_char": start,
                "end_char": end,
                "length": len(chunk)
            })
        
        return result
    
    def chunk_with_metadata(self, text: str, metadata: Dict = None) -> List[Dict]:
        """分块并携带原始元数据"""
        chunks = self.chunk_text(text)
        for chunk in chunks:
            if metadata:
                chunk["metadata"] = metadata
            else:
                chunk["metadata"] = {}
        return chunks