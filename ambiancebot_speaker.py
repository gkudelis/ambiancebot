import time
from random import randint

from twython import Twython
from twython.exceptions import TwythonError
from dynamodb_mapper.model import ConnectionBorg

import settings
from digram import Digram


cb = ConnectionBorg()
cb.set_region('eu-west-1')
cb.set_credentials(settings.aws_access_key_id, settings.aws_secret_access_key)

t = Twython(settings.app_key,
        settings.app_secret,
        settings.oauth_token,
        settings.oauth_token_secret)

while True:
    tweet = ''
    last_word = ''

    # get all digrams in db
    ds = Digram.scan()
    # count total number of digrams on the db
    total_count = 0
    for d in ds:
        total_count += d.count
    # pick a random digram
    r = randint(1, total_count)
    print 'r = '+str(r)
    ds = Digram.scan()
    csum = 0
    for d in ds:
        csum += d.count
        print 'csum = '+str(csum)
        if r <= csum:
            tweet += d.w1 + ' ' + d.w2
            last_word = d.w2
            print last_word
            break

    # third word
    ds = Digram.query(last_word)
    total_count = 0
    for d in ds:
        total_count += d.count
    if total_count == 0:
        continue
    r = randint(1, total_count)
    ds = Digram.query(last_word)
    csum = 0
    for d in ds:
        csum += d.count
        if r <= csum:
            tweet += ' ' + d.w2
            last_word = d.w2
            break

    # fourth word
    ds = Digram.query(last_word)
    total_count = 0
    for d in ds:
        total_count += d.count
    if total_count == 0:
        continue
    r = randint(1, total_count)
    ds = Digram.query(last_word)
    csum = 0
    for d in ds:
        csum += d.count
        if r <= csum:
            tweet += ' ' + d.w2
            last_word = d.w2
            break

    print "tweeting '" + tweet + "'"
    t.update_status(status=tweet)

    time.sleep(5*60)
