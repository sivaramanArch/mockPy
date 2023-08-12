from dependency_injector import containers, providers
import falcon
from modules import DB_Handler
from wsgiref import simple_server


class HttpServer:
    def __init__(self) -> None:
        self.app = falcon.App()

    def add_route(self, route, resource) -> None:
        self.app.add_route(route, resource=resource)

    def launch(self):
        httpd = simple_server.make_server('127.0.0.1', 8000, self.app)
        print("Serving on http://127.0.0.1:8000")
        httpd.serve_forever()


class Repository:
    def __init__(self):
        self.db_path = "db.json"
        self.driver = DB_Handler(self.db_path)

    def get(self):
        return self.driver.get_all()

    def get_by_key(self, key):
        return self.driver.get_by_key(key)

    def insert(self, key, value):
        self.driver.write_by_key(key=key, new_object=value)


class AppContainer(containers.DeclarativeContainer):
    repository = providers.Singleton(Repository)
    http_server = providers.Factory(HttpServer)
