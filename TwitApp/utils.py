import os
import tweepy


def twit_auth_handler():
    cons_tok = 'foVcRMOv9MD7sB63dZDwhATOq'
    cons_sec ='j4ke4amMa1ydFmgBXKTDBgcr8fcxNtvRgFOhiyja2PR2NbYy94'
    app_tok = '2923384237-Z3B7GDEXG3p9ioNhc2KKKUXaYHjWpsGXBhb2mkN'
    app_sec = 'bkl5hC9qPjYF0Hen5pYJvYFfIyN39BoWnVNc9SlgHqiFV'
    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    auth.set_access_token(app_tok, app_sec)

    return tweepy.API(auth)
