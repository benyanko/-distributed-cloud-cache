from flask import Flask
from flask_restful import Api



def create_app():

    app = Flask(__name__)
    api = Api()
    api.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")

