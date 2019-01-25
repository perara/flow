import numpy as np

class PerSerializer:

    @staticmethod
    def serialize(message):

        if type(message) == np.ndarray:
            b = message.tobytes()
            b_l = len(b)

        else:
            raise NotImplementedError("The type %s is not implemented in PerSerializer" % type(data))

    @staticmethod
    def deserialize(data):
        pass
