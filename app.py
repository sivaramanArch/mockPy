import json
from modules import AppContainer
import sys


def main(config_file):
    with open(config_file) as json_file:
        property_map = json.load(json_file)

    container = AppContainer()

    container.app_launcher(property_map)
    container.api_config().setup()
    container.server().launch()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage python app.py <path_to_env.json>")

    else:
        config_file = sys.argv[1]
        main(config_file)
