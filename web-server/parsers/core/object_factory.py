class ObjectFactory:
    def __init__(self):
        self.builders = {}

    def register_builder(self, key, builder):
        self.builders[key] = builder

    def create(self, key, **kwargs):
        builder = self.builders.get(key)
        if not builder:
            raise ValueError(f"No builder registered for key: {key}")
        return builder(**kwargs)
