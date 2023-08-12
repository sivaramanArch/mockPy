import yaml

from modules import AppContainer, dynamic_controller

app_container = AppContainer()

http_server = app_container.http_server()
repo = app_container.repository()

api_config_path = 'api.yaml'


def process_domain(domain):
    id = domain.get("id", None)
    route = domain.get("slug", "/")
    methods = domain.get("expose", [])

    http_server.add_route(route, dynamic_controller(id, methods, repo))


def traverse_domain(data):
    print(f"recieved domain data : {data}")

    if isinstance(data, dict):
        for k, v in data.items():
            print(f"Identified key : {k}")
            if isinstance(v, dict):
                process_domain(v)


def traverse_config(api_config):
    if not isinstance(api_config, dict):
        raise Exception("Malformed yaml")

    domains = api_config.get("domain", [])

    if not isinstance(domains, list):
        raise Exception("Domain is expected to be a list")

    for domain in domains:
        traverse_domain(domain)


def configure_api():
    with open(api_config_path, 'r') as api_config:
        traverse_config(yaml.safe_load(api_config))


if __name__ == '__main__':
    configure_api()
    http_server.launch()
