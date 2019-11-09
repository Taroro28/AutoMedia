# coding: UTF-8
import tweepy, config, time, schedule, re
import datetime as dt

# TwitterAPI
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth)

# 自分について
my_api = api.me()
my_id = my_api.id
my_screen_name = my_api.screen_name

def job():
    # 自分のタイムライン
    results = api.user_timeline(screen_name= my_screen_name, count=100, tweet_mode='extended')

    tweet_list = []

    for result in results:
        if not '@' in result.full_text:
            tweet_list.append(result.full_text)

    latest_tweet = re.sub(r'https.+$', '', tweet_list.pop(0))

    for index, tweet in enumerate(tweet_list):
        if re.sub(r'https.+$', '', tweet) == latest_tweet:
            api.update_status(tweet_list[index-1])
            print("ツイートしました")
            print(dt.datetime.now())
            break

# 毎日15:00に実行
schedule.every().day.at("15:00").do(job)

while True:
    schedule.run_pending()
    # スリープごとに確認
    time.sleep(60)