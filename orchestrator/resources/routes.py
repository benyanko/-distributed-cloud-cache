from flask_restful import Api

from orchestrator.resources.nodes import Node


def register_routes(api: Api):
    api.add_resource(Node, "/nodes")
