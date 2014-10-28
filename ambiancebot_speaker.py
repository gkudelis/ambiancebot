import dbm, time
from twython import Twython
from twython.exceptions import TwythonError

db = dbm.open('words', 'r')

t = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

while True:
    max_count = 0
    max_word = ''
    runner_up = ''
    for w in db.keys():
        w_count = int(db[w])
        if w_count > max_count:
            max_count = w_count
            runner_up = max_word
            max_word = w
    try:
        t.update_status(status=max_word)
    except TwythonError:
        t.update_status(status=runner_up)

    time.sleep(10*60)
