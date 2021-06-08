from flask import request, current_app
from flask_restful import Resource
from cache_node.models import LRUCache


class Clean(Resource):
    def post(self):
        LRUCache.cache.clean()
        return {"msg": "clean cache"}, 200, ({"Content-Type": "application/json"})
