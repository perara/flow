import flatbuffers
import numpy as np


from serializers.flatbuffers import Numpy


class FlatbufferSerializer:

    def __init__(self):
        pass

    @staticmethod
    def serialize(data):

        if type(data) == np.ndarray:
            # Serialize numpy array
            builder = flatbuffers.Builder(data.nbytes)

            Numpy.NumpyStart(builder)
            builder.CreateNumpyVector(data.flatten())

            serialized = Numpy.NumpyEnd(builder)




        else:
            raise NotImplementedError("The type %s is not implemented in FlatbufferSerializer" % type(data))
    @staticmethod
    def deserialize(data):
        pass