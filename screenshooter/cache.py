import time
from typing import NamedTuple


class Result(NamedTuple):
    end_time: int
    created: bool


class Cache:
    def __init__(self, ttl: int):
        self.ttl = ttl
        self.storage: dict[int, int] = {}

    def add(self, hash_: int) -> int:
        t = int(time.time()) + self.ttl
        self.storage[hash_] = t
        return t

    def get(self, hash_: int) -> Result:
        t: int = self.storage.get(hash_, None)
        if t is None or int(time.time()) > t:
            new_t = self.add(hash_)
            return Result(new_t, False)
        return Result(t, True)
