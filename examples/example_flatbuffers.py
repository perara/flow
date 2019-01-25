from serializers.flatbuffers.spec import FlatbufferSerializer

if __name__ == "__main__":
    import numpy as np

    data = np.random.rand(80, 80, 3)

    FlatbufferSerializer.serialize(data)

