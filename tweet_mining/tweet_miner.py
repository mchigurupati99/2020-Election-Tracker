import os

import tweepy
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Import statement for local modules on PyCharm
# from tweet_mining.utils import pick_random_coordinate, utc_to_local, build_connection_string
# from tweet_mining.sentiment_analysis.sentiment import text_to_sentiment


# Import statement for local modules on Anaconda
from utils import pick_random_coordinate, utc_to_local, build_connection_string
from sentiment_analysis.sentiment import text_to_sentiment


class Tweet:
    """ A class used to represent tweet data as an object """

    def __init__(self, candidate, user_name, text, sentiment_score, tokens, date, location, favorite_count,
                 retweet_count):
        """
        Tweet constructor
        :param candidate: Candidate associated with the tweet
        :type candidate: str
        :param user_name: User who posted the tweet
        :type user_name: str
        :param text: Body of the tweet
        :type text: str
        :param sentiment_score: Score rating the sentiment of the tweet
        :type sentiment_score: float
        :param tokens: List of key words extracted from the tweet
        :type tokens: lst(str)
        :param date: Date and time the tweet was created
        :type date: datetime.datetime
        :param location:  Latitude and longitude of where the tweet was posted
        :type location: list(float)
        :param favorite_count: Number of favorites the tweet received
        :type favorite_count: int
        :param retweet_count: Number of retweets the tweet received
        :type retweet_count: int
        """
        self.candidate = candidate
        self.user_name = user_name
        self.text = text
        self.sentiment_score = sentiment_score
        self.tokens = tokens
        self.date = date
        self.location = location
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count

    def format_json(self):
        """
        Converts the Tweet object into a dictionary
        """
        return {'candidate': self.candidate, 'user_name': self.user_name, 'text': self.text,
                'sentiment_score': self.sentiment_score, 'tokens': self.tokens, 'date': self.date,
                'location': self.location, 'favorite_count': self.favorite_count, 'retweet_count': self.retweet_count}


# Loading authentication keys to access the Twitter API
load_dotenv()
auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Connecting to the MongoDB database
client = MongoClient(build_connection_string())
db = client["election"]
collection = db["tweets"]


def mine_candidate_tweets(candidates, start_date, end_date, count):
    """
    Mines tweets related to the given candidates in a certain date range
    and writes them to a MongoDB database

    :param candidates: Names of candidates to mine related tweets
    :type candidates: list(str)
    :param start_date: Lower bound of the date range
    :param start_date: datetime.datetime()
    :param end_date: Upper bound of the date range
    :param end_date: datetime.datetime()
    :param count: Number of tweets to search through
    :param count: int
    :return: Tuple containing the number of tweets mined
             and the number of tweets that had a location
    :rtype: tuple(int)
    """
    tweets_mined = 0
    tweets_with_location = 0
    for candidate in candidates:
        for tweet in tweepy.Cursor(api.search, q=candidate, tweet_mode='extended').items(count):

            tweets_mined += 1
            # Tweepy returns date in UTC time, need to convert to local time
            local_date = utc_to_local(tweet.created_at)

            # Tweet is in date range
            if True:
            # if start_date <= local_date <= end_date:
                # Tweet has a location tagged
                if tweet.coordinates is not None or tweet.place is not None:
                    tweets_with_location += 1

                    if tweet.coordinates is not None:
                        location = tweet.coordinates['coordinates']
                    else:
                        location = pick_random_coordinate(tweet.place.bounding_box.coordinates[0])

                    # Tweepy returns location as (longitude, latitude), need to swap
                    location.reverse()

                    # Analyzing sentiment of the Tweet
                    sentiment_return = text_to_sentiment(tweet.full_text)
                    sentiment_score = sentiment_return[0]
                    tokens = sentiment_return[1]

                    # Tweet does not contain any valid words
                    if len(tokens) == 0:
                        continue

                    tweet_object = Tweet(candidate, tweet.user.name, tweet.full_text, sentiment_score, tokens,
                                         local_date, location, tweet.favorite_count, tweet.retweet_count)

                    # Inserting Tweet data into the database
                    collection.insert_one(tweet_object.format_json())
                    print(candidate + ' tweet mined!')
                    print(tweets_mined)
                    print(tweets_with_location)

    return tweets_mined, tweets_with_location


candidates = ['donald trump']
start_date = datetime(2020, 4, 20, 0, 0, 0, 0)
end_date = datetime(2020, 4, 20, 23, 59, 59, 999999)
# end_date = datetime(2020, 4, 11, 23, 59, 59, 999999)
mine_candidate_tweets(candidates, start_date, end_date, 10000)
