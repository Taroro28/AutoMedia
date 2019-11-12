# coding: UTF-8
import tweepy, config, time, schedule, re
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

    # my timeline
    # tweet_mode='extended' for get full text
    # count is amount of tweets
    my_timeline = api.user_timeline(screen_name= my_screen_name, count=100, tweet_mode='extended')

    # tweets without retweet, reply and quote
    tweet_list = []
    for tweet in my_timeline:
        if not '@' in tweet.full_text:
            tweet_list.append(tweet.full_text)

    # latest tweet which text has URL
    latest_tweet = re.sub(r'https.+$', '', tweet_list.pop(0))

    # tweet the text of next day of the day when I tweeted the same text before.
    for index, tweet in enumerate(tweet_list):
        # same as latest tweet
        if re.sub(r'https.+$', '', tweet) == latest_tweet:
            # tweet tweet of next day of that day
            api.update_status(tweet_list[index-1])

            # validation on terminal
            print("No Problem!", dt.datetime.now())
            break

# run every 15:00
schedule.every().day.at("15:00").do(job)

# check the task every minute
while True:
    schedule.run_pending()
    time.sleep(60)
