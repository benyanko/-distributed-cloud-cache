import enum

import typing

from orchestrator.node.utils import node_lock


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NodeState(enum.Enum):
    DOWN = 0
    RUNNING = 1


class Node:
    def __init__(self, url):
        self.url = url
        self._state = NodeState.RUNNING

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val: NodeState):
        self._state = val


class NodeRegistry(metaclass=Singleton):

    sub_cluster_size = 2

    def __init__(self):
        self.size = 0
        self._registry: typing.MutableMapping[int, Node] = {}
        self._id_url_mapping: typing.MutableMapping[str, id] = {}

    def add_node(self, url: str):
        acquired = node_lock.acquire(timeout=5)
        if acquired:
            node_id = self._get_down_node()
            if node_id:
                node_id = self.size
                self.size += 1
            self._registry[node_id] = Node(url=url)
            self._id_url_mapping[url] = self.size
        else:
            raise RuntimeError

    def get_nodes(self, key: str) -> typing.List[Node]:
        if self.size < self.sub_cluster_size:
            raise RuntimeError(f"not enough node registered {self.sub_cluster_size - self.size} missing")

        first_node_id = self.__key_to_id(key=key)
        nodes = []
        for i in range(self.sub_cluster_size):
            node = self._registry[first_node_id % self.size]
            if node.state == NodeState.RUNNING:
                nodes.append(node)
            first_node_id += 1
        return nodes

    def __key_to_id(self, key) -> int:
        return (hash(key) & ((1 << 16) - 1)) % self.size

    def set_node_down(self, url: str):
        self._registry[self._id_url_mapping[url]].state = NodeState.DOWN

    def _get_down_node(self) -> typing.Optional[int]:
        for node_id, node in self._registry.items():
            if node.state == NodeState.DOWN:
                return node_id

        return None
