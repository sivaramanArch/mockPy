import yaml
from modules import DynamicHttpController
from modules import AppLauncher


class BootstrapService:
    def __init__(self, app_launcher: AppLauncher, server, repo) -> None:
        self.api_config_path = app_launcher.get_api_spec()
        self.server = server
        self.repo = repo

    def setup(self):
        with open(self.api_config_path, 'r') as api_config:
            self._traverse_config(yaml.safe_load(api_config))

    def _traverse_config(self, api_config):
        if not isinstance(api_config, dict):
            raise Exception("Malformed yaml")

        domains = api_config.get("domain", [])

        if not isinstance(domains, list):
            raise Exception("Domain is expected to be a list")

        for domain in domains:
            self._traverse_domain(domain)

    def _traverse_domain(self, data):
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"Identified resource : {k}")
                if isinstance(v, dict):
                    self._process_domain(v)

    def _process_domain(self, domain):
        id = domain.get("id", None)
        route = domain.get("slug", "/")
        methods = domain.get("expose", [])
        tuple_id = domain.get("uuid", None)

        self.repo.create_key(id)

        resource = DynamicHttpController(id, methods, self.repo, tuple_id)

        self.server.add_route(route, resource)
