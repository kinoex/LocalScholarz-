import pdfplumber
import re
from typing import List, Dict

class PDFParser:
    """PDF解析器：提取文本、标题、段落结构"""
    
    def __init__(self):
        self.full_text = ""
        self.pages = []
        self.metadata = {}
    
    def parse(self, file_path: str) -> Dict:
        """解析PDF，返回结构化内容"""
        result = {
            "text": "",
            "pages": [],
            "metadata": {},
            "sections": []
        }
        
        with pdfplumber.open(file_path) as pdf:
            # 提取元数据
            result["metadata"] = {
                "pages": len(pdf.pages),
                "title": pdf.metadata.get("Title", "未知标题"),
                "author": pdf.metadata.get("Author", "未知作者")
            }
            
            # 逐页提取文本
            full_text = ""
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
                    result["pages"].append({
                        "page_num": i + 1,
                        "text": text
                    })
            
            result["text"] = full_text
            
        # 尝试提取章节标题（简单版：找"摘要"、"引言"等关键词）
        result["sections"] = self._extract_sections(full_text)
        
        return result
    
    def _extract_sections(self, text: str) -> List[Dict]:
        """简易章节抽取（用关键词匹配）"""
        keywords = ["摘要", "引言", "方法", "实验", "结果", "讨论", "结论", 
                    "Abstract", "Introduction", "Method", "Experiment", 
                    "Result", "Discussion", "Conclusion"]
        
        sections = []
        lines = text.split("\n")
        for i, line in enumerate(lines):
            line_clean = line.strip()
            # 匹配关键词开头的行（且长度不超过50，大概率是标题）
            for kw in keywords:
                if line_clean.startswith(kw) and len(line_clean) < 50:
                    sections.append({
                        "title": line_clean,
                        "start_line": i,
                        "content": "\n".join(lines[i:i+5])[:200] + "..."  # 预览
                    })
                    break
        return sections