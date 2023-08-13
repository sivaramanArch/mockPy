import falcon
import json


class DynamicHttpController:
    def __init__(self, id, methods, repo):
        self.id = id
        self.methods = methods
        self.repo = repo

    def on_get(self, req, resp):
        if "GET" not in self.methods:
            resp.status = falcon.HTTP_403
            resp.message = "Method not supported"
            return

        resp.status = falcon.HTTP_200
        resp.media = self.repo.get_by_key(self.id)

    def on_post(self, req, resp):
        if "POST" not in self.methods:
            resp.status = falcon.HTTP_403
            resp.message = "Method not supported"
            return

        data = json.loads(req.bounded_stream.read().decode('utf-8'))
        resp.status = falcon.HTTP_201
        self.repo.insert(key=self.id, value=data)
        resp.media = data
