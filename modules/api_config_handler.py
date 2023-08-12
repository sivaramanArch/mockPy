
import yaml
from modules import DynamicHttpController


class ApiConfigurer:
    def __init__(self, path, server, repo) -> None:
        self.api_config_path = path
        self.server = server
        self.repo = repo

    def process_domain(self, domain):
        id = domain.get("id", None)
        route = domain.get("slug", "/")
        methods = domain.get("expose", [])

        resource = DynamicHttpController(id, methods, self.repo)
        self.server.add_route(route, resource)

    def traverse_domain(self, data):
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"Identified key : {k}")
                if isinstance(v, dict):
                    self.process_domain(v)

    def traverse_config(self, api_config):
        if not isinstance(api_config, dict):
            raise Exception("Malformed yaml")

        domains = api_config.get("domain", [])

        if not isinstance(domains, list):
            raise Exception("Domain is expected to be a list")

        for domain in domains:
            self.traverse_domain(domain)

    def setup(self):
        with open(self.api_config_path, 'r') as api_config:
            self.traverse_config(yaml.safe_load(api_config))
