import datetime

from flask import request, current_app
from flask_restful import Resource


class Cache(Resource):
    def get(self):

        return {"msg": "ok"}, 200, ({"Content-Type": "application/json"})

    def post(self):

        return {"msg": "ok"}, 200, ({"Content-Type": "application/json"})
