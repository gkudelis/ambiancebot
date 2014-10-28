import settings

import time, sqlite3
from random import randint

from twython import Twython
from twython.exceptions import TwythonError


db = sqlite3.connect('words.db')
c = db.cursor()

t = Twython(settings.app_key,
        settings.app_secret,
        settings.oauth_token,
        settings.oauth_token_secret)

lastword = ''
while True:
    # get total count of words in db
    c.execute("SELECT SUM(cnt) FROM words")
    total_count, = c.fetchone()

    new_word_found = False
    while not new_word_found:
        # pick a random number
        r = randint(1, total_count)

        # go over results and pick one
        csum = 0
        for word, cnt in c.execute("SELECT word, cnt FROM words"):
            csum += cnt
            if r <= csum:
                break

        # check if the chosen word is not the same as previous one
        if word != lastword:
            new_word_found = True

    print "trying to tweet '" + word + "'"
    t.update_status(status=word)
    lastword = word

    time.sleep(10*60)
