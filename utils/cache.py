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