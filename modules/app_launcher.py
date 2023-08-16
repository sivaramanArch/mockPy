class AppLauncher:

    """
        Accepts the env variable properties as a dict instance
        Configures the instance to hold the properties in memory
    """

    def __init__(self, property_map: dict) -> None:
        self._version = property_map.get("version", "-1")
        self._api = property_map.get("apiSpec")
        self._db = property_map.get("db")
        self._default_class_path = property_map.get("classPath")

        print(f"Configuring MockPy version {self._version}")

    def get_api_spec(self) -> str:
        return self._api

    def get_db(self) -> str:
        return self._db
