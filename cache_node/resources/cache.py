import requests

from flask_restful import Resource


class Cache(Resource):
    def get(self, key):
        response = requests.get("/orchestrator/node", json={"key": key})
        json = response.json()
        urls = json["urls"]

        for url in urls:
            try:
                resp = requests.get(url + "/cache-strict", json={"key": key})
                if resp.ok:
                    return resp.json(), 200, ({"Content-Type": "application/json"})
            except requests.RequestException:
                # TODO add orc url
                requests.post(f"orc_url/check/", json={"url": url})

            return {"data": None}, 200, ({"Content-Type": "application/json"})

    def put(self, key, data, expiration_date):
        response = requests.get("/orchestrator/node")
        json = response.json()
        urls = json["urls"]

        for url in urls:
            try:
                _ = requests.post(url + "/cacheStrict", json={"key": key, "data": data, "expiration_date": expiration_date})
                return {"msg": "ok"}
            except requests.RequestException:
                # TODO:
                #  add orc url
                requests.post("/orchestrator/check/", json={"url": url})
                pass
