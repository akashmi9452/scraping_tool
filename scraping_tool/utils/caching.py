import redis

class CacheManager:
    def __init__(self, redis_host: str, redis_port: int):
        self.client = redis.Redis(host=redis_host, port=redis_port)

    def get_cache(self, key: str):
        value = self.client.get(key)
        return float(value) if value else None

    def set_cache(self, key: str, value: float):
        self.client.set(key, value)
