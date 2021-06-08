import datetime

from cache_node.models import LRUCache
from flask_restful import Resource


class CacheStrict(Resource):
    def get(self, key):
        data = LRUCache.cache.get(key)
        if data:
            return {"data": data}, 200, ({"Content-Type": "application/json"})
        return {"msg": None}, 400, ({"Content-Type": "application/json"})

    def put(self, key, data, expiration_date):
        LRUCache.cache.set(key, data, expiration_date)
        return {"data": data}, 200, ({"Content-Type": "application/json"})
