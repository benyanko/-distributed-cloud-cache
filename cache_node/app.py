import os
import sys
import requests
from flask import Flask
from flask_restful import Api
from .resources.routes import register_routes


def create_app():

    app = Flask(__name__)
    api = Api()
    register_routes(api)
    api.init_app(app)

    URL = os.getenv()
    response = requests.get('/orchestrator/node', json={'url': URL})
    if response.ok:
        return app
    else:
        sys.exit(1)


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")

