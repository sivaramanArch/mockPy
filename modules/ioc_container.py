from dependency_injector import containers, providers
import falcon
from modules import DB_Handler
from wsgiref import simple_server
from modules import BootstrapService


class HttpServer:
    def __init__(self) -> None:
        self.app = falcon.App()

    def add_route(self, route, resource) -> None:
        print(f"Registering route : {route}")
        self.app.add_route(route, resource=resource)

    def launch(self, port=8080):
        httpd = simple_server.make_server('127.0.0.1', port, self.app)
        print(f"Serving on http://127.0.0.1:{port}")
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

    def delete(self, key, value):
        self.driver.delete(key=key, record=value)


class AppContainer(containers.DeclarativeContainer):
    repository = providers.Singleton(Repository)
    server = providers.Singleton(HttpServer)
    api_config = providers.Factory(
        BootstrapService, "api.yaml", server, repository)
