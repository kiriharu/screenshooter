import time


class Cache:

    def __init__(self, ttl: int):
        self.ttl = ttl
        self.storage: dict[int, int] = {}

    def add(self, hash_: int):
        self.storage[hash_] = int(time.time()) + self.ttl

    def get(self, hash_: int) -> int:
        """End time if in cache, 0 if created"""
        t = self.storage.get(hash_, None)
        if t is None or int(time.time()) > t:
            self.add(hash_)
            return 0
        return t
