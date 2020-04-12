import tweepy

CONSUMER_KEY = "3ZqrtNWdxN4ncSO9xt4JYhNAs"
CONSUMER_SECRET_KEY = "A0gpo0fnqancEoB49edAPMQrCnypSaMnyGUOHLCfIDaHVYunmrz"
ACCESS_TOKEN = "1248785120418361346-HNOywGyiTh7hdHwZbg941QhQUOwsnh"
ACCESS_TOKEN_SECRET = "K1NCqigovmYvOfvkd0trE8XfsiBmyqxZbyLEiGxn1dfkw"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

twitter_api = tweepy.API(auth)
