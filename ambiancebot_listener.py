import re

from twython import TwythonStreamer
from dynamodb_mapper.model import ConnectionBorg
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError

import settings
from trigram import Trigram


cb = ConnectionBorg()
cb.set_region('eu-west-1')
cb.set_credentials(settings.aws_access_key_id, settings.aws_secret_access_key)

class InStream(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print "analyzing '" + data['text'] + "'"
            # find words
            ws = filter(lambda match: match != '',
                re.findall(r"$| ([a-zA-Z-']+)", data['text'].encode('utf-8')))
            # turn into lower case words
            ws = map(lambda word: word.lower(), ws)

            # trigrams please
            trigrams = reduce(
                lambda tris, w: tris + [(tris[-1][1], tris[-1][2], w)],
                ws, [('','','')])[3:]
            print "found trigrams: " + str(trigrams)

            for tg in trigrams:
                try:
                    t_rec = Trigram.get(tg[0]+','+tg[1], tg[2])
                except DynamoDBKeyNotFoundError:
                    t_rec = Trigram()
                    t_rec.w12 = tg[0]+','+tg[1]
                    t_rec.w3 = tg[2]
                t_rec.count += 1
                t_rec.save()

    def on_error(self, status_code, data):
        print status_code

s = InStream(settings.app_key,
        settings.app_secret,
        settings.oauth_token, 
        settings.oauth_token_secret)

s.statuses.filter(track='@ambiancebot')
