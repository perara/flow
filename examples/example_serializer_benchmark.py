import pickle

import numpy as np
import json
import ujson
import rapidjson
import marshal
import time
import marshmallow

class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)



if __name__ == "__main__":

    def benchmark(name, fn, count=1):
        s = time.time_ns()
        for x in range(count):
            fn()
        end = time.time_ns() - s
        print("[%s]: Count=%s, Time=%sms" % (name, count, int(end / 1000000)))

    class Data:

        def __init__(self, size):
            self.data = np.random.rand(size, size)
            self.type = "TestMessage"
            self.cmd = "get_test"


    to_be_serialized = Data(50)

    def standard_json_serialize():
        json.dumps(to_be_serialized.__dict__, cls=NumPyArangeEncoder)

    def ujson_serialize():
        ujson.dumps(to_be_serialized.__dict__,)

    def rapidjson_serialize():
        rapidjson.dumps(to_be_serialized.__dict__, cls=NumPyArangeEncoder)

    def pickle_serialize():
        pickle.dumps(to_be_serialized)

    def pickle_dict_serialize():
        pickle.dumps(to_be_serialized)

    def marshal_serialize():
        x = marshal.dumps(to_be_serialized.__dict__)
        y = marshal.loads(x)
        print(y)
    benchmark("json", standard_json_serialize, count=1000)
    benchmark("ujson", ujson_serialize, count=1000)
    #benchmark("rapidjson", rapidjson_serialize, count=1000)
    benchmark("pickle", pickle_serialize, count=1000)
    benchmark("pickle_dict", pickle_dict_serialize, count=1000)
    benchmark("marshal", marshal_serialize, count=1000)




