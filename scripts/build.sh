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
