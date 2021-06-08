import threading

import requests
from flask_restful import Resource, reqparse

from orchestrator.node import utils as node_utils
from orchestrator.node.node_registry import NodeRegistry
from orchestrator.node.utils import node_lock


class Node(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("key", type=str, required=True, help="key attribute is missing or invalid", location="json")

    def get(self):
        args = self.parser.parse_args()
        node_registry = NodeRegistry()
        try:
            nodes_url = [node.url for node in node_registry.get_nodes(args["key"])]
            return nodes_url, 200
        except RuntimeError:
            return {"msg": "not fully initiated"}, 500


class NodeCheck(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="url attribute is missing or invalid", location="json")

    def post(self):
        acquired = node_lock.acquire(timeout=5)
        if acquired:
            args = self.parser.parse_args()
            try:
                requests.get(f"{args['url']}/heartbeat")
            except requests.RequestException:
                t = threading.Thread(target=node_utils.deploy_node, daemon=True)
                t.start()

            return {"msg": "checked"}, 200
        else:
            return {"msg": "could not check"}, 400


class NodeRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="url attribute is missing or invalid", location="json")

    def post(self):
        args = self.parser.parse_args()
        node_registry = NodeRegistry()
        node_registry.add_node(args["url"])
        return {"msg": "registered"}




