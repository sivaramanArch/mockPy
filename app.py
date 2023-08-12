from modules import AppContainer

container = AppContainer()

server = container.server()
api_config = container.api_config()

if __name__ == '__main__':
    api_config.setup()
    server.launch()
