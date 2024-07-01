from parsers.core.object_factory import ObjectFactory

PARSERS_FACTORY = ObjectFactory()
PARSED_OBJECTS_FACTORY = ObjectFactory()


def register_parsers_builder(key):
    def decorator(cls):
        PARSERS_FACTORY.register_builder(key.value, cls())
        return cls

    return decorator


def register_parsed_objects_builder(key):
    def decorator(cls):
        PARSED_OBJECTS_FACTORY.register_builder(key.value, cls())
        return cls

    return decorator
