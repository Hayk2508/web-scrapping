from core.object_factory import ObjectFactory

FACTORY = ObjectFactory()


def register_builder(key):
    def decorator(cls):
        FACTORY.register_builder(key, cls())
        return cls

    return decorator
