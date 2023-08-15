import json
from functools import lru_cache


class DB_Handler:
    def __init__(self, file_path):
        if file_path == None:
            raise Exception("File path is mandatory")

        self.file_path = file_path
        self.indent = 4

    def get_all(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON from file: {e}")
            return None

    def get_by_key(self, key):
        return self.get_all().get(key)

    def refresh_store(self, data):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=self.indent)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error updating JSON file: {e}")

    def write_by_key(self, key, new_object):
        if not isinstance(new_object, dict):
            raise Exception("Object is expected to be KV compliant")

        data = self.get_all()

        if key in data and isinstance(data[key], list):
            data[key].append(new_object)
        else:
            data[key] = [new_object]

        self.refresh_store(data=data)

    def delete(self, key, record):
        if not isinstance(record, dict):
            raise Exception("Object is expected to be a dict")

        all_records = self.get_all()

        if key in all_records and isinstance(all_records[key], list):
            all_records[key] = [_ for _ in all_records[key] if _ != record]

        self.refresh_store(data=all_records)
