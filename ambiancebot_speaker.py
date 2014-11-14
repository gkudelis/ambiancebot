import time
from random import randint

from twython import Twython
from twython.exceptions import TwythonError
from dynamodb_mapper.model import ConnectionBorg

import settings
from trigram import Trigram


cb = ConnectionBorg()
cb.set_region('eu-west-1')
cb.set_credentials(settings.aws_access_key_id, settings.aws_secret_access_key)

tw = Twython(settings.app_key,
        settings.app_secret,
        settings.oauth_token,
        settings.oauth_token_secret)

while True:
    try:
        tweet = ''
        last_word = ''

        # get all digrams in db
        ts = Trigram.scan()
        # count total number of digrams on the db
        total_count = 0
        for t in ts:
            total_count += t.count
        # pick a random digram
        r = randint(1, total_count)
        print 'r = '+str(r)
        ts = Trigram.scan()
        csum = 0
        for t in ts:
            csum += t.count
            print 'csum = '+str(csum)
            if r <= csum:
                tweet += ' '.join(t.w12.split(','))
                last_pair = (t.w12.split(',')[1], t.w3)
                break

        while len(tweet)+len(last_pair[1])+1 <= 80:
            tweet += ' ' + last_pair[1]

            ts = Trigram.query(','.join(last_pair))
            total_count = 0
            for t in ts:
                total_count += t.count
            if total_count == 0:
                break
            r = randint(1, total_count)
            ts = Trigram.query(','.join(last_pair))
            csum = 0
            for t in ts:
                csum += t.count
                if r <= csum:
                    last_pair = (t.w12.split(',')[1], t.w3)
                    break

        print "tweeting '" + tweet + "'"
        tw.update_status(status=tweet)
    except TwythonError:
        time.sleep(60)
    else:
        # 1/6 chance to tweet every 1/6th of the set interval
        tweet_again = False
        while not tweet_again:
            time.sleep(settings.interval*10)
            tweet_again = (randint(1,6) == 6)
