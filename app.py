from modules import AppContainer

app_container = AppContainer()

http_server = app_container.http_server()
api_configurer = app_container.api_configurer()

if __name__ == '__main__':
    http_server.launch()
