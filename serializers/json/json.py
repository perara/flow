import ujson


class FastJSONSerializer:

    @staticmethod
    def serialize(message):
        return ujson.dumps(message)

    @staticmethod
    def deserialize(message):
        return ujson.loads(message)
