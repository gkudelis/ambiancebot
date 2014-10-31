from dynamodb_mapper.model import DynamoDBModel

class Trigram(DynamoDBModel):
    __table__ = u"trigrams"
    __hash_key__ = u"w12"
    __range_key__ = u"w3"
    __schema__ = {
        u"w12": str,
        u"w3": str,
        u"count": int,
    }
    __defaults__ = {
        u"count": 0,
    }
