from serializers.perializer.PerSerializer import PerSerializer as Serializer
from serializers.json.json import FastJSONSerializer as Serializer
if __name__ == "__main__":
    import numpy as np

    data = np.random.rand(80, 80, 3)

    d = Serializer.serialize(data)