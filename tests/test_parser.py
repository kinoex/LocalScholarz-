import pytest
from core.parser import PDFParser
import tempfile

def test_parser_metadata():
    """测试PDF解析元数据"""
    parser = PDFParser()

    # 创建测试PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    result = parser.parse(tmp_path)
    assert "metadata" in result
    assert "pages" in result["metadata"]

    import os
    os.unlink(tmp_path)
