from flask_restful import Api

from .cache import Cache
from .cache_strict import CacheStrict
from .clean import Clean
from .heartbeat import Heartbeat


def register_routes(api: Api):
    api.add_resource(Cache, "/cache")
    api.add_resource(CacheStrict, "/cacheStrict")
    api.add_resource(Clean, "/clean")
    api.add_resource(Heartbeat, "/")
