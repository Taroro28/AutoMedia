import tweepy, config, time, schedule
import datetime as dt

# Twitter API
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth)

# my account
my_api = api.me()
my_id = my_api.id
my_screen_name = my_api.screen_name

def job():
    today = dt.date.today()

    # my_timeline(default count=0)
    my_timeline = api.user_timeline(screen_name= my_screen_name)

    for my_tweet in my_timeline:
        # tweeted time
        tweeted_time = my_tweet.created_at + dt.timedelta(hours=9)

        # if tweeted time is  between 15:00 and 15:02 today
        if tweeted_time.date() == today and tweeted_time.hour == 15 and tweeted_time.minute < 2:
            # retweet
            api.retweet(my_tweet.id)

            # like
            api.create_favorite(my_tweet.id)

            # validation on terminal
            print("No Problem!", dt.datetime.now())

            break

# run every 19:00
schedule.every().day.at("19:00").do(job)

# check the task every minute
while True:
    schedule.run_pending()
    time.sleep(60)
