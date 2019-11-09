import tweepy, config, time, schedule
import datetime as dt

# Twitter APIの認証
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
    today = dt.date.today()

    # 自分のタイムライン
    results = api.user_timeline(screen_name= my_screen_name)

    for result in results:
        # ツイートされた時間
        created_time = result.created_at + dt.timedelta(hours=9)

        # 当日の15時にツイートされたツイートをいいねしてリツイート
        if created_time.date() == today and created_time.hour == 15 and created_time.minute < 2:
            api.retweet(result.id)
            api.create_favorite(result.id)
            print("リツイートしました")
            print(dt.datetime.now())
            break

# 毎日19:00に実行
schedule.every().day.at("19:00").do(job)


while True:
    schedule.run_pending()
    # スリープごとに確認
    time.sleep(60)
