from flask import Flask
from flask_restful import Api

from orchestrator.resources.routes import register_routes


def create_app():

    app = Flask(__name__)
    api = Api()
    register_routes(api=api)
    api.init_app(app=app)

    return app