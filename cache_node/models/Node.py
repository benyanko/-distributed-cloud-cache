class Node:
    def __init__(self, key, data, expiration_date):
        self.key = key
        self.data = data
        self.expiration_date = expiration_date
        self.prev = None
        self.next = None
