import settings
from digram import Digram

import time
from random import randint

from dynamodb_mapper.model import ConnectionBorg

from twython import Twython
from twython.exceptions import TwythonError

cb = ConnectionBorg()
cb.set_region('eu-west-1')
cb.set_credentials(settings.aws_access_key_id, settings.aws_secret_access_key)

t = Twython(settings.app_key,
        settings.app_secret,
        settings.oauth_token,
        settings.oauth_token_secret)

while True:
    try:
        # get total count of words in db
        c.execute("SELECT SUM(cnt) FROM words")
        total_count, = c.fetchone()

        # pick a random number
        r = randint(1, total_count)

        # go over results and pick one
        csum = 0
        for word, cnt in c.execute("SELECT word, cnt FROM words"):
            csum += cnt
            if r <= csum:
                break

        print "trying to tweet '" + word + "'"
        t.update_status(status=word)
    except TwythonError:
        time.sleep(60)
    else:
        time.sleep(10*60)
