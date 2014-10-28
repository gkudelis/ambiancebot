import settings
import re, sqlite3
from twython import TwythonStreamer

db = sqlite3.connect('words.db')
c = db.cursor()

class InStream(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print "analyzing '" + data['text'] + "'"
            ws = filter(lambda match: match != '',
                re.findall(r'$| ([a-zA-Z-]+)', data['text'].encode('utf-8')))
            for w in map(lambda word: word.lower(), ws):
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
