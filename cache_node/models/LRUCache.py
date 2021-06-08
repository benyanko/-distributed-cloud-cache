import datetime

from cache_node.models import Node


class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.count = 0

    def deleteNode(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def addToHead(self, node):
        node.next = self.head.next
        node.next.prev = node
        node.prev = self.head
        self.head.next = node

    def clean(self):
        for node in self.map:
            if node.expiration_date < datetime.datetime.utcnow().isoformat():
                self.deleteNode(node)

    def get(self, key):
        if key in self.map:
            node = self.map[key]
            result = node.data
            self.deleteNode(node)
            self.addToHead(node)
            return result
        return -1

    def set(self, key, data):
        if key in self.map:
            node = self.map[key]
            node.data = data
            self.deleteNode(node)
            self.addToHead(node)
        else:
            node = Node(key, data)
            self.map[key] = node
            if self.count < self.capacity:
                self.count += 1
                self.addToHead(node)
            else:
                del self.map[self.tail.prev.key]
                self.deleteNode(self.tail.prev)
                self.addToHead(node)

