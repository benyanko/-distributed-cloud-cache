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

    # TODO: need to verify env var name
    URL = os.getenv("SERVER_URL")
    try:
        response = requests.get("/orchestrator/node", json={"url": URL})
    except requests.RequestException:
        sys.exit(1)
    else:
        if response.ok:
            return app
        else:
            sys.exit(1)


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
