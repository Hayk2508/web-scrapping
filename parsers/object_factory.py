class ObjectFactory:
    def __init__(self):
        self.builders = {}

    def register_builder(self, key, builder):
        self.builders[key] = builder

    def create(self, key, **kwargs):
        builder = factory.builders.get(key)
        if not builder:
            raise ValueError(f"No builder registered for key: {key}")
        return builder(**kwargs)


def initialize_factory():
    return ObjectFactory()


factory = initialize_factory()


def register_builder(key):
    def decorator(cls):
        factory.register_builder(key, cls())
        return cls

    return decorator
