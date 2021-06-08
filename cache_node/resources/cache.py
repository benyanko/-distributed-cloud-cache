import requests

from flask_restful import Resource


class Cache(Resource):
    def get(self, key):
        response = requests.get('/orchestrator/node', json={'key': key})
        json = response.json()
        urls = json['urls']

        for url in urls:
            try:
                return requests.get(url+'/cacheStrict', json={'key': key})
            except ConnectionError:
                requests.post('/orchestrator/check/', json={'url': url})
                return {"msg": ConnectionError.__str__()}, 400, ({"Content-Type": "application/json"})

    def put(self, key, data, expiration_date):
        response = requests.get('/orchestrator/node')
        json = response.json()
        urls = json['urls']

        for url in urls:
            try:
                return requests.post(url+'/cacheStrict', json={'key': key,
                                                               'data': data,
                                                               'expiration_date': expiration_date})
            except ConnectionError:
                requests.post('/orchestrator/check/', json={'url': url})
                return {"msg": ConnectionError.__str__()}, 400, ({"Content-Type": "application/json"})
