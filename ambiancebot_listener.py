import re

from twython import TwythonStreamer
from dynamodb_mapper.model import ConnectionBorg
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError

import settings
from digram import Digram


cb = ConnectionBorg()
cb.set_region('eu-west-1')
cb.set_credentials(settings.aws_access_key_id, settings.aws_secret_access_key)

class InStream(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print "analyzing '" + data['text'] + "'"
            # find words
            ws = filter(lambda match: match != '',
                re.findall(r'$| ([a-zA-Z-]+)', data['text'].encode('utf-8')))
            # turn into lower case words
            ws = map(lambda word: word.lower(), ws)

            # digrams please
            digrams = reduce(lambda dis, w: dis + [(dis[-1][1], w)], ws, [('','')])[2:]
            print "found digrams: " + str(digrams)

            for di in digrams:
                try:
                    d_rec = Digram.get(di[0], di[1])
                except DynamoDBKeyNotFoundError:
                    d_rec = Digram()
                    d_rec.w1 = di[0]
                    d_rec.w2 = di[1]
                d_rec.count += 1
                d_rec.save()

    def on_error(self, status_code, data):
        print status_code

s = InStream(settings.app_key,
        settings.app_secret,
        settings.oauth_token, 
        settings.oauth_token_secret)

s.statuses.filter(track='@ambiancebot')
