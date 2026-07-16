from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Tuple

class LocalEmbedder:
    """本地向量嵌入 + FAISS存储"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        模型选项（按推荐度）：
        - all-MiniLM-L6-v2: 轻量最快，384维，中文可用
        - paraphrase-multilingual-MiniLM-L12-v2: 多语言，384维
        - BAAI/bge-small-zh: 中文专用，512维
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.chunks = []
        self.index_path = "data/faiss_index"
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """批量向量化"""
        return self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True  # 便于余弦相似度
        )
    
    def build_index(self, chunks: List[Dict]):
        """构建FAISS索引"""
        self.chunks = chunks
        texts = [c["text"] for c in chunks]
        
        print(f"正在向量化 {len(texts)} 个文本块...")
        embeddings = self.embed_texts(texts)
        
        # 创建FAISS索引
        self.index = faiss.IndexFlatIP(self.dimension)  # 内积索引（归一化后=余弦）
        self.index.add(embeddings)
        
        print(f"✅ 索引构建完成，共 {self.index.ntotal} 个向量")
        
        # 保存索引和元数据
        self.save()
        
    def save(self):
        """保存到本地"""
        os.makedirs("data", exist_ok=True)
        faiss.write_index(self.index, f"{self.index_path}.faiss")
        with open(f"{self.index_path}.pkl", "wb") as f:
            pickle.dump({
                "chunks": self.chunks,
                "dimension": self.dimension
            }, f)
        print(f"💾 已保存到 {self.index_path}")
    
    def load(self):
        """加载本地索引"""
        if not os.path.exists(f"{self.index_path}.faiss"):
            print("⚠️ 未找到索引文件，请先构建")
            return False
        
        self.index = faiss.read_index(f"{self.index_path}.faiss")
        with open(f"{self.index_path}.pkl", "rb") as f:
            data = pickle.load(f)
            self.chunks = data["chunks"]
            self.dimension = data["dimension"]
        print(f"✅ 加载索引成功，共 {self.index.ntotal} 个向量")
        return True
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """检索最相关的文本块"""
        if self.index is None:
            self.load()
        
        # 向量化查询
        query_vec = self.model.encode([query], normalize_embeddings=True)
        
        # 搜索
        scores, indices = self.index.search(query_vec, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunks):
                results.append((self.chunks[idx], float(score)))
        
        return results