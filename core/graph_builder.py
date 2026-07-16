import jieba
import jieba.posseg as pseg
import re
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import json

class GraphBuilder:
    """从论文文本中抽取实体和关系，构建知识图谱"""
    
    def __init__(self):
        # 技术领域关键词词典（可扩展）
        self.tech_keywords = {
            "AI", "人工智能", "机器学习", "深度学习", "神经网络", "NLP", 
            "自然语言处理", "CV", "计算机视觉", "强化学习", "迁移学习",
            "Transformer", "BERT", "GPT", "LLM", "大语言模型", "RAG",
            "CNN", "RNN", "LSTM", "GAN", "扩散模型", "多模态"
        }
        
        # 关系模板（正则匹配）
        self.relation_patterns = [
            (r"(\S+?)是(\S+?)的", "is_a"),           # A是B的
            (r"(\S+?)包括(\S+?)", "includes"),       # A包括B
            (r"(\S+?)分为(\S+?)", "divided_into"),   # A分为B
            (r"(\S+?)提出(\S+?)", "proposed"),       # A提出B
            (r"(\S+?)使用(\S+?)", "uses"),           # A使用B
            (r"(\S+?)优于(\S+?)", "better_than"),    # A优于B
            (r"(\S+?)基于(\S+?)", "based_on"),       # A基于B
        ]
        
        self.entities = []  # 所有实体
        self.relations = []  # 所有关系三元组 (头, 关系, 尾)
        self.entity_types = {}  # 实体类型映射
    
    def extract_entities(self, text: str) -> List[Dict]:
        """抽取实体：技术名词 + 人名 + 机构名"""
        entities = []
        seen = set()
        
        # 1. 用jieba做词性标注
        words = pseg.cut(text)
        for word, flag in words:
            # 过滤短词和停用词
            if len(word) < 2:
                continue
            if word in {"的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"}:
                continue
            
            entity = word.strip()
            if entity in seen:
                continue
            seen.add(entity)
            
            # 判断类型
            entity_type = self._classify_entity(entity, flag)
            if entity_type:
                entities.append({
                    "name": entity,
                    "type": entity_type,
                    "frequency": text.count(entity)  # 简单频次
                })
        
        # 2. 补充技术关键词匹配（更精确）
        for keyword in self.tech_keywords:
            if keyword in text and keyword not in seen:
                entities.append({
                    "name": keyword,
                    "type": "技术概念",
                    "frequency": text.count(keyword)
                })
                seen.add(keyword)
        
        # 按频次排序，保留高频实体
        entities.sort(key=lambda x: x["frequency"], reverse=True)
        self.entities = entities[:50]  # 最多保留50个
        
        return self.entities
    
    def _classify_entity(self, word: str, pos_flag: str) -> str:
        """分类实体类型"""
        # 基于词性
        if pos_flag in ['nr', 'nrt']:  # 人名
            return "人名"
        if pos_flag in ['ns']:  # 地名
            return "机构/地名"
        if pos_flag in ['nz']:  # 专有名词
            return "专有名词"
        if pos_flag in ['n', 'vn']:  # 名词
            # 检查是否是技术术语
            if word in self.tech_keywords or any(kw in word for kw in self.tech_keywords):
                return "技术概念"
            return "一般名词"
        
        # 基于关键词匹配
        if word in self.tech_keywords:
            return "技术概念"
        if "大学" in word or "学院" in word or "研究院" in word:
            return "机构"
        if "教授" in word or "博士" in word or "研究" in word:
            return "人物"
        
        return "其他"
    
    def extract_relations(self, text: str, entities: List[Dict]) -> List[Dict]:
        """抽取实体间关系（基于共现和模式匹配）"""
        relations = []
        entity_names = [e["name"] for e in entities]
        
        # 方法1：基于关系模板
        for pattern, rel_type in self.relation_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 2:
                    head, tail = match[0], match[1]
                    if head in entity_names and tail in entity_names:
                        relations.append({
                            "head": head,
                            "relation": rel_type,
                            "tail": tail,
                            "source": "pattern_match"
                        })
        
        # 方法2：基于共现（同一句子中出现的实体对）
        sentences = re.split(r'[。！？；\n]', text)
        for sent in sentences:
            sent_entities = [e for e in entity_names if e in sent]
            if len(sent_entities) >= 2:
                # 两两组合
                for i in range(len(sent_entities)):
                    for j in range(i+1, len(sent_entities)):
                        # 检查是否已在relations中
                        exists = False
                        for r in relations:
                            if (r["head"] == sent_entities[i] and r["tail"] == sent_entities[j]) or \
                               (r["head"] == sent_entities[j] and r["tail"] == sent_entities[i]):
                                exists = True
                                break
                        if not exists:
                            relations.append({
                                "head": sent_entities[i],
                                "relation": "共现",
                                "tail": sent_entities[j],
                                "source": "co-occurrence",
                                "context": sent[:100] + "..."
                            })
        
        self.relations = relations
        return relations
    
    def build_graph(self, text: str) -> Dict:
        """完整构建知识图谱"""
        print("🔍 正在抽取实体...")
        entities = self.extract_entities(text)
        print(f"   ✅ 抽取到 {len(entities)} 个实体")
        
        print("🔗 正在抽取关系...")
        relations = self.extract_relations(text, entities)
        print(f"   ✅ 抽取到 {len(relations)} 条关系")
        
        return {
            "entities": entities,
            "relations": relations,
            "stats": {
                "entity_count": len(entities),
                "relation_count": len(relations),
                "entity_types": self._count_types(entities)
            }
        }
    
    def _count_types(self, entities: List[Dict]) -> Dict:
        """统计实体类型分布"""
        types = defaultdict(int)
        for e in entities:
            types[e["type"]] += 1
        return dict(types)
    
    def to_json(self, filepath: str = "data/graph.json"):
        """导出为JSON"""
        data = {
            "entities": self.entities,
            "relations": self.relations
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 图谱已导出到 {filepath}")