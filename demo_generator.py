import hashlib
import pickle
import os
from functools import lru_cache
from typing import Any, Callable
import time

class CacheManager:
    """文件缓存管理器，避免重复计算"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_hash(self, key: str) -> str:
        """生成哈希作为文件名"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Any:
        """获取缓存"""
        hash_key = self._get_hash(key)
        path = os.path.join(self.cache_dir, f"{hash_key}.pkl")
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return pickle.load(f)
            except:
                return None
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        hash_key = self._get_hash(key)
        path = os.path.join(self.cache_dir, f"{hash_key}.pkl")
        with open(path, "wb") as f:
            pickle.dump(value, f)
    
    def clear(self):
        """清空缓存"""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir, exist_ok=True)


# 装饰器版缓存
def cache_result(cache_dir: str = "data/cache"):
    def decorator(func: Callable):
        cache = CacheManager(cache_dir)
        
        def wrapper(*args, **kwargs):
            # 生成缓存key（基于函数名和参数）
            key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            result = cache.get(key)
            if result is not None:
                print(f"⚡ 从缓存加载: {func.__name__}")
                return result
            
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        
        return wrapper
    return decorator
2. 优化后的解析器 core/parser_fast.py（增量版）
python
import pdfplumber
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from utils.cache import cache_result

class FastPDFParser:
    """多线程PDF解析器（大文件优化）"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    @cache_result()
    def parse(self, file_path: str) -> Dict:
        """带缓存的解析"""
        result = {
            "text": "",
            "pages": [],
            "metadata": {}
        }
        
        with pdfplumber.open(file_path) as pdf:
            # 元数据
            result["metadata"] = {
                "pages": len(pdf.pages),
                "title": pdf.metadata.get("Title", "未知标题"),
                "author": pdf.metadata.get("Author", "未知作者")
            }
            
            # 多线程提取文本（大文件）
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                for page in pdf.pages:
                    futures.append(executor.submit(self._extract_page, page))
                
                for i, future in enumerate(futures):
                    text = future.result()
                    if text:
                        result["pages"].append({
                            "page_num": i + 1,
                            "text": text
                        })
                        result["text"] += text + "\n"
        
        return result
    
    @staticmethod
    def _extract_page(page):
        try:
            return page.extract_text()
        except:
            return ""
📦 第二步：打包和发布
1. setup.py（PyPI打包）
python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="local-scholar",
    version="0.1.0",
    author="Your Name",
    description="纯本地论文精读助手，支持知识图谱和智能问答",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kineox/local-scholar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.35.0",
        "pdfplumber>=0.11.0",
        "langchain>=0.2.0",
        "sentence-transformers>=2.3.0",
        "faiss-cpu>=1.8.0",
        "jieba>=0.42.1",
        "pyvis>=0.3.2",
        "ollama>=0.2.1",
        "numpy>=1.26.0",
    ],
    entry_points={
        "console_scripts": [
            "local-scholar=app:main",
        ],
    },
)
2. scripts/build.sh（一键构建）
bash
#!/bin/bash

echo "📦 构建 LocalScholar..."

# 1. 清理旧文件
rm -rf dist/ build/ *.egg-info

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试
pytest tests/ -v

# 4. 打包
python setup.py sdist bdist_wheel

# 5. 生成文档
python scripts/demo_generator.py

echo "✅ 构建完成！"
echo "📁 安装包: dist/"
echo "📄 文档: docs/"
3. scripts/demo_generator.py（Demo视频生成脚本）
python
"""生成项目Demo截图和GIF"""

import os
import subprocess

def generate_demo():
    """自动生成演示素材"""
    
    print("🎬 生成演示素材...")
    
    # 1. 截图
    os.makedirs("demo", exist_ok=True)
    
    # 使用pyautogui自动截图（需安装）
    try:
        import pyautogui
        import time
        
        # 启动应用
        subprocess.Popen(["streamlit", "run", "app.py"])
        time.sleep(3)
        
        # 截图
        screenshot = pyautogui.screenshot()
        screenshot.save("demo/screenshot_1.png")
        print("✅ 截图已保存")
        
    except:
        print("⚠️ 自动截图失败，请手动截图")
    
    # 2. 生成README用的徽章
    badges = """
    ![Python Version](https://img.shields.io/badge/python-3.8+-blue)
    ![License](https://img.shields.io/badge/license-MIT-green)
    ![Stars](https://img.shields.io/github/stars/kineox/local-scholar)
    ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)
    """
    with open("demo/badges.md", "w") as f:
        f.write(badges)
    
    print("✅ 演示素材生成完成！")

if __name__ == "__main__":
    generate_demo()