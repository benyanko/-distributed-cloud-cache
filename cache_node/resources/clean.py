import datetime

from flask import request, current_app
from flask_restful import Resource


class Clean(Resource):
    def post(self):

        return {"msg": "ok"}, 200, ({"Content-Type": "application/json"})
