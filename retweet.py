import tweepy, config, time, schedule
import datetime as dt

"""
"""
def job():
    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, ATS)

    api = tweepy.API(auth)
    maro = api.me()
    my_id = maro.id
    my_screen_name = maro.screen_name

    today = dt.date.today()

    results = api.user_timeline(screen_name= my_screen_name)

    for result in results:
        created_time = result.created_at + dt.timedelta(hours=9)
        if created_time.date() == today and created_time.hour == 15 and created_time.minute < 2:
            api.retweet(result.id)
            api.create_favorite(result.id)
            print("リツイートしました")
            print(dt.datetime.now())

schedule.every().day.at("19:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
