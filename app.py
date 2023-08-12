import falcon
import json
from wsgiref import simple_server
import yaml


class HelloWorldResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.text = "Hello, World!"


# Create a Falcon app
app = falcon.App()

# Define the route and attach the HelloWorldResource
app.add_route('/', HelloWorldResource())


def main(app):
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    print("Serving on http://127.0.0.1:8000")

    httpd.serve_forever()


def read_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON from file: {e}")
        return None


def add_object_to_json(key, new_object, file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        if key in data and isinstance(data[key], list):
            data[key].append(new_object)
        else:
            data[key] = [new_object]

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print(f"Object added to '{key}' in '{file_path}'")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error updating JSON file: {e}")


def write_to_store(file_path, key, obj):
    add_object_to_json(key=key, new_object=obj, file_path=file_path)


def read_all(id):
    return read_json_from_file("db.json").get(id, None)


def persist(id, data):
    add_object_to_json(id, data, "db.json")


def create_dynamic_class(class_name, methods, id):
    class DynamicClass:
        def __init__(self, id, methods):
            self.id = id
            self.methods = methods

        def on_get(self, req, resp):
            if "GET" not in methods:
                raise Exception("Method not supported on resource")

            resp.status = falcon.HTTP_200
            resp.media = read_all(self.id)

        def on_post(self, req, resp):
            if "POST" not in methods:
                raise Exception("POST Method not supported on resource")
            
            data = json.loads(req.bounded_stream.read().decode('utf-8'))
            resp.status = falcon.HTTP_201
            persist(id=self.id, data=data)
            resp.media = data

    DynamicClass.__name__ = class_name  # Set the class name
    return DynamicClass(id=id, methods=methods)


def create_resource(id, methods):
    return create_dynamic_class(id+"Resource", methods=methods, id=id)


def create_api(id, route, methods):
    resource = create_resource(id, methods)
    app.add_route(route, resource=resource)


def process_domain(domain):
    print(f"Domain data recieved : {domain}")
    id = domain.get("id", None)
    route = domain.get("slug", "/")
    methods = domain.get("expose", [])
    create_api(id, route, methods)


def traverse_domain(data, indent=0):
    print(f"recieved domain data : {data}")

    if isinstance(data, dict):
        for k, v in data.items():
            print(f"Identified key : {k}")
            if isinstance(v, dict):
                process_domain(v)


def traverse_yaml(data, indent=0):
    if not isinstance(data, dict):
        raise Exception("Malformed yaml")

    domains = data.get("domain", [])

    if not isinstance(domains, list):
        raise Exception("Domain is expected to be a list")

    for domain in domains:
        traverse_domain(domain, indent+1)


if __name__ == '__main__':
    # main(app)
    with open('api.yaml', 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        traverse_yaml(yaml_data)

    main(app=app)
