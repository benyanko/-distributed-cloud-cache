import datetime

from cache_node.models import Node


class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head = Node(0, 0, datetime.datetime.utcnow().isoformat())
        self.tail = Node(0, 0, datetime.datetime.utcnow().isoformat())
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

    def get(self, key):
        if key in self.map:
            node = self.map[key]
            if node.expiration_date >= datetime.datetime.utcnow().isoformat():
                result = node.data
                self.deleteNode(node)
                self.addToHead(node)
                return result
            else:
                self.deleteNode(node)
        return None

    def set(self, key, data, expiration_date):
        if key in self.map:
            node = self.map[key]
            node.data = data
            self.deleteNode(node)
            self.addToHead(node)
        else:
            node = Node(key, data, expiration_date)
            self.map[key] = node
            if self.count < self.capacity:
                self.count += 1
                self.addToHead(node)
            else:
                del self.map[self.tail.prev.key]
                self.deleteNode(self.tail.prev)
                self.addToHead(node)

    def clean(self):
        for node in self.map:
            if node.expiration_date < datetime.datetime.utcnow().isoformat():
                self.deleteNode(node)


cache = LRUCache(1000)
