from pymongo import MongoClient
from datetime import datetime
from tweet_mining.utils import build_connection_string


def get_tweet_collection():
    """
    Obtains the tweet collection from the election database

    :return: tweets collection
    :rtype: pymongo.collection.Collection
    """
    client = MongoClient(build_connection_string())
    database = client['election']
    tweet_collection = database['tweets']
    return tweet_collection


def get_request_times(api_request):
    """
    Parses the start and end dates from query parameters of a request

    :param api_request: request from an api call
    :type api_request: werkzeug.local.LocalProxy
    :return: status code, start datetime, and end datetime
    :rtype: tuple(str, datetime.datetime, datetime.datetime)
    """
    # properly formatted query parameters will have a start and end key
    query_dict = api_request.args.to_dict()
    start_date = query_dict.get('start', None)
    end_date = query_dict.get('end', None)

    if start_date is None or end_date is None:
        return "Error", None, None

    # convert string to a datetime object
    start_datetime = datetime.strptime(start_date, '%m/%d/%Y')
    end_datetime = datetime.strptime(end_date, '%m/%d/%Y')

    # set the end datetime to 11:59:59 PM
    end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
    return "Ok", start_datetime, end_datetime
