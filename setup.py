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