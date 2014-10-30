from dynamodb_mapper.model import DynamoDBModel

class Digram(DynamoDBModel):
    __table__ = u"digrams"
    __hash_key__ = u"w1"
    __range_key__ = u"w2"
    __schema__ = {
        u"w1": str,
        u"w2": str,
        u"count": int,
    }
    __defaults__ = {
        u"count": 0,
    }
