import ollama
from typing import List, Dict, Optional

class OllamaClient:
    """本地模型调用封装"""
    
    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model
        self.check_model()
    
    def check_model(self):
        """检查模型是否存在"""
        try:
            models = ollama.list()
            model_names = [m["name"] for m in models["models"]]
            if self.model not in model_names:
                print(f"⚠️ 模型 {self.model} 未安装，请运行: ollama pull {self.model}")
                return False
            print(f"✅ 模型 {self.model} 已就绪")
            return True
        except Exception as e:
            print(f"⚠️ Ollama连接失败: {e}")
            return False
    
    def chat(self, messages: List[Dict], stream: bool = False, **kwargs):
        """对话接口"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                stream=stream,
                **kwargs
            )
            return response
        except Exception as e:
            print(f"❌ 调用失败: {e}")
            return None
    
    def generate_answer(self, context: str, query: str, max_tokens: int = 500) -> str:
        """基于上下文生成答案（论文问答专用）"""
        prompt = f"""你是一个专业的学术论文精读助手。请基于以下论文内容回答用户的问题。

        ## 论文内容片段
        {context}

        ## 用户问题
        {query}

        ## 要求
        1. 只基于提供的内容回答，不要臆测
        2. 如果内容中没有相关信息，请明确告知
        3. 回答要简洁、准确、有条理

        ## 回答
        """
        
        messages = [
            {"role": "system", "content": "你是一个严谨的学术助手，擅长精读论文并回答问题。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat(messages)
        if response:
            return response["message"]["content"]
        return "⚠️ 模型调用失败，请检查Ollama是否运行"