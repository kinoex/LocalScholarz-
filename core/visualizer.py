from pyvis.network import Network
import json
import os
from typing import List, Dict

class GraphVisualizer:
    """知识图谱可视化（生成交互式HTML）"""
    
    def __init__(self):
        self.net = None
    
    def visualize(self, entities: List[Dict], relations: List[Dict], 
                  output_path: str = "data/graph.html", height: str = "750px"):
        """生成交互式知识图谱HTML"""
        
        # 创建网络
        self.net = Network(
            height=height,
            width="100%",
            bgcolor="#ffffff",
            font_color="black",
            directed=True
        )
        
        # 添加节点（实体）
        for entity in entities:
            # 根据类型设置颜色
            color = self._get_color(entity.get("type", "其他"))
            size = 20 + min(entity.get("frequency", 1) * 2, 30)  # 频次越高节点越大
            
            self.net.add_node(
                entity["name"],
                label=entity["name"],
                title=f"{entity['name']}\n类型: {entity.get('type', '未知')}\n频次: {entity.get('frequency', 1)}",
                color=color,
                size=size
            )
        
        # 添加边（关系）
        for relation in relations:
            # 关系粗细基于置信度
            width = 2 if relation.get("source") == "pattern_match" else 1
            
            self.net.add_edge(
                relation["head"],
                relation["tail"],
                label=relation["relation"],
                title=f"{relation['head']} → {relation['tail']}\n关系: {relation['relation']}",
                width=width,
                arrowStrikethrough=False
            )
        
        # 设置物理引擎（更好的布局）
        self.net.set_options("""
        var options = {
            "physics": {
                "enabled": true,
                "stabilization": {
                    "iterations": 100
                },
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "centralGravity": 0.01,
                    "springLength": 100,
                    "springConstant": 0.08
                }
            },
            "interaction": {
                "hover": true,
                "tooltipDelay": 100
            }
        }
        """)
        
        # 保存
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.net.save_graph(output_path)
        print(f"✅ 图谱已保存到 {output_path}")
        return output_path
    
    def _get_color(self, entity_type: str) -> str:
        """根据实体类型返回颜色"""
        colors = {
            "技术概念": "#FF6B6B",  # 红
            "人名": "#4ECDC4",      # 青
            "机构": "#45B7D1",      # 蓝
            "专有名词": "#96CEB4",   # 绿
            "一般名词": "#FFEAA7",  # 黄
            "其他": "#DDA0DD"       # 紫
        }
        return colors.get(entity_type, "#DDA0DD")
    
    def from_json(self, json_path: str = "data/graph.json", output_html: str = "data/graph.html"):
        """从JSON文件加载并可视化"""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.visualize(data["entities"], data["relations"], output_html)