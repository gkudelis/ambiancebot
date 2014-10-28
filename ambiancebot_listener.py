import settings
import re, sqlite3
from twython import TwythonStreamer

db = sqlite3.connect('words.db')
c = db.cursor()

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

            # record findings
            for w in ws:
                c.execute("SELECT cnt FROM words WHERE word=?", (w,))
                try:
                    cnt, = c.fetchone()
                    c.execute("UPDATE words SET cnt=? where word=?", (cnt+1, w))
                except TypeError:
                    c.execute("INSERT INTO words (word, cnt) VALUES (?, 1)", (w,))
                db.commit()


    def on_error(self, status_code, data):
        print status_code

s = InStream(settings.app_key,
        settings.app_secret,
        settings.oauth_token, 
        settings.oauth_token_secret)

s.statuses.filter(track='@ambiancebot')
