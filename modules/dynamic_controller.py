import falcon
import json


class DynamicHttpController:
    def __init__(self, id, methods, repo, tuple_id=None):
        self.id = id
        self.methods = methods
        self.repo = repo
        self.tuple_id = tuple_id

    def on_get(self, req, resp):
        if "GET" not in self.methods:
            resp.status = falcon.HTTP_403
            resp.body = "Method not supported"
            return

        resp.status = falcon.HTTP_200
        resp.media = self.repo.get_by_key(self.id)

    def on_post(self, req, resp):
        if "POST" not in self.methods:
            resp.status = falcon.HTTP_403
            resp.body = "Method not supported"
            return
        data = json.loads(req.bounded_stream.read().decode('utf-8'))
        self._insert(data, resp)

    def on_put(self, req, resp):
        if "PUT" not in self.methods:
            resp.status = falcon.HTTP_403
            resp.body = "Method not supported"
            return

        all_records: list = self.repo.get_by_key(self.id)
        data = json.loads(req.bounded_stream.read().decode('utf-8'))

        record_id = data.get(self.tuple_id, None)

        does_exits = self.tuple_id and record_id and next(
            (obj for obj in all_records if obj['id'] == record_id), None)

        if does_exits:
            resp.status = falcon.HTTP_201
            resp.media = data

        else:
            self._insert(data, resp)

    def _insert(self, data, resp):
        resp.status = falcon.HTTP_201
        self.repo.insert(key=self.id, value=data)
        resp.media = data
