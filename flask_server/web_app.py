from flask import Flask, jsonify, request, render_template, json
import requests
from datetime import datetime, timedelta

from flask_server.utils import get_tweet_collection, get_request_times

# HTTP Status Codes
OK = 200
CREATED = 201
BAD_REQUEST = 400
UNSUPPORTED_MEDIA_TYPE = 415

LOCAL_HOST = 'http://127.0.0.1:5000'

app = Flask(__name__)

tweet_collection = get_tweet_collection()


# Entry point for web app
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # GET request when web app is first loaded
        return render_template('index.html', marker_map=json.dumps({}), time_series=json.dumps({}),
                               word_cloud=json.dumps({}))

    # obtaining text submission from frontend
    date_range = request.form.to_dict()['daterange']
    start_date, end_date = date_range.split('-')

    # removing extra spaces
    start_date = start_date[:-1]
    end_date = end_date[1:]

    # creating API endpoints to retrieve data
    tweet_info_request = LOCAL_HOST + '/api/tweetInfo?start=' + start_date + '&end=' + end_date
    sentiment_ratings_request = LOCAL_HOST + '/api/sentimentRatings?start=' + start_date + '&end=' + end_date
    tokens_request = LOCAL_HOST + '/api/tokens?start=' + start_date + '&end=' + end_date

    # making GET requests to API
    marker_map_data = requests.get(tweet_info_request).json()
    time_series_data = requests.get(sentiment_ratings_request).json()
    word_cloud_data = requests.get(tokens_request).json()

    return render_template('index.html', marker_map=json.dumps(marker_map_data),
                           time_series=json.dumps(time_series_data), word_cloud=json.dumps(word_cloud_data)), OK


# API Endpoints
@app.route("/api/tweetInfo/")
def get_tweet_info():
    (status, start_datetime, end_datetime) = get_request_times(request)
    if status == "Error":
        return "start date and/or end date not specified", BAD_REQUEST

    # find tweets from both candidates that are within the date range
    query = {'date': {'$gte': start_datetime, '$lte': end_datetime}}

    # project all attributes except for id
    projection = {'_id': 0}

    queried_tweets = list(tweet_collection.find(query, projection))
    return jsonify(queried_tweets), OK


@app.route("/api/sentimentRatings/")
def get_sentiment_ratings():
    (status, start_datetime, end_datetime) = get_request_times(request)
    if status == "Error":
        return "start date and/or end date not specified", BAD_REQUEST

    # query for finding tweets for the democratic and republican candidate in the date range
    dem_query = {'date': {'$gte': start_datetime, '$lte': end_datetime}, 'candidate': 'joe biden'}
    rep_query = {'date': {'$gte': start_datetime, '$lte': end_datetime}, 'candidate': 'donald trump'}

    # only want to retrieve the candidate and sentiment score for each tweet
    projection = {'_id': 0, 'candidate': 1, 'sentiment_score': 1, 'date': 1}

    dem_queried_tweets = list(tweet_collection.find(dem_query, projection))
    rep_queried_tweets = list(tweet_collection.find(rep_query, projection))

    total_days = int((end_datetime - start_datetime).days) + 1

    # storing all dates between the start and end date range
    dates = []
    for num_days in range(total_days):
        incremented_datetime = start_datetime + timedelta(days=num_days)
        incremented_date = str(incremented_datetime.month) + '/' + str(incremented_datetime.day)
        dates.append(incremented_date)

    # no tweets were found in the date range
    if len(dem_queried_tweets) == 0 and len(dem_queried_tweets) == 0:
        return {'dates': dates, 'dem': [], 'rep': []}

    # maintain a list of sentiment scores for each day in the date range
    # 0th index represents the start date, last index represents the end date
    dem_sentiment = [[] for _ in range(total_days)]
    rep_sentiment = [[] for _ in range(total_days)]

    # storing sentiment of each tweet in the appropriate day
    for dem_tweet in dem_queried_tweets:
        day_diff = int((end_datetime - dem_tweet['date']).days)
        dem_sentiment[total_days - day_diff - 1].append(dem_tweet['sentiment_score'])
    for rep_tweet in rep_queried_tweets:
        day_diff = int((end_datetime - rep_tweet['date']).days)
        rep_sentiment[total_days - day_diff - 1].append(rep_tweet['sentiment_score'])

    # compute average sentiment score for each day
    for day in range(total_days):
        dem_sentiment[day] = sum(dem_sentiment[day]) / len(dem_sentiment[day])
        rep_sentiment[day] = sum(rep_sentiment[day]) / len(rep_sentiment[day])

    sentiment_ret = {'dates': dates, 'dem': dem_sentiment, 'rep': rep_sentiment}
    return jsonify(sentiment_ret), OK


@app.route("/api/tokens/")
def get_tokens():
    (status, start_datetime, end_datetime) = get_request_times(request)
    if status == "Error":
        return "start date and/or end date not specified", BAD_REQUEST

    # query for finding tweets for the democratic and republican candidate in the date range
    dem_query = {'date': {'$gte': start_datetime, '$lte': end_datetime}, 'candidate': 'joe biden'}
    rep_query = {'date': {'$gte': start_datetime, '$lte': end_datetime}, 'candidate': 'donald trump'}

    # only want to retrieve the candidate and token list for each tweet
    projection = {'_id': 0, 'candidate': 1, 'tokens': 1}

    dem_queried_tweets = list(tweet_collection.find(dem_query, projection))
    rep_queried_tweets = list(tweet_collection.find(rep_query, projection))

    dem_word_count = {}
    rep_word_count = {}
    for tweet in dem_queried_tweets:
        for token in tweet['tokens']:
            dem_word_count[token] = 1 + dem_word_count.get(token, 0)
    for tweet in rep_queried_tweets:
        for token in tweet['tokens']:
            rep_word_count[token] = 1 + rep_word_count.get(token, 0)
    dem_list = [{'word': token, 'size': count} for token, count in dem_word_count.items()]
    rep_list = [{'word': token, 'size': count} for token, count in rep_word_count.items()]

    # # push all tokens from each tweet into a list of tokens for each candidate
    # dem_tokens = [token for tweet in dem_queried_tweets for token in tweet['tokens']]
    # rep_tokens = [token for tweet in rep_queried_tweets for token in tweet['tokens']]
    dem_list = sorted(dem_list, key=lambda x: x['size'], reverse=True)[:50]
    rep_list = sorted(rep_list, key=lambda x: x['size'], reverse=True)[:50]
    token_ret = {'dem': dem_list, 'rep': rep_list}
    return jsonify(token_ret), OK


if __name__ == "__main__":
    app.run(debug=True)
