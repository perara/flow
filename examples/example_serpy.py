import serpy


class Message(serpy.Serializer):
    type = serpy.StrField()
    message = serpy.Field()


class Data:
    type = "hello"
    message = "world"

data = {
    "type": "Hello",
    "message": "world"
}



print(dir(Message(Data())))