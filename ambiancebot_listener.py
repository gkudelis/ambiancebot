import dbm, re
from twython import TwythonStreamer

db = dbm.open('words', 'c')

class InStream(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            ws = filter(lambda match: match != '',
                re.findall(r'$| ([a-zA-Z-]+)', data['text'].encode('utf-8')))
            for w in map(lambda word: word.lower(), ws):
                try:
                    current_count = int(db[w])
                except KeyError:
                    current_count = 0
                db[w] = str(current_count + 1)
            print 'I have these keys: ' + str(db.keys())

    def on_error(self, status_code, data):
        print status_code

s = InStream(app_key, app_secret, oauth_token, oauth_token_secret)

s.statuses.filter(track='@ambiancebot')
