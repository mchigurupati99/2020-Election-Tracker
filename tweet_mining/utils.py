import random
import os

from datetime import timezone
from dotenv import load_dotenv


def utc_to_local(utc_date_time):
    """
    Takes a datetime object in UTC time and converts it to local time

    :param utc_date_time: Datetime in UTC time
    :param utc_date_time: datetime.datetime()
    :return: Input datetime converted to local time
    :rtype: datetime.datetime()
    """
    return (utc_date_time.replace(tzinfo=timezone.utc).astimezone(tz=None)).replace(tzinfo=None)


def pick_random_coordinate(coordinates):
    """
    Picks a random coordinate given a coordinate area to select from

    :param coordinates: List of four coordinates that make up a rectangular area
    :return: Longitude and latitude of the random coordinate selected
    :rtype: list(float)
    """
    lower_long = coordinates[0][0]
    lower_lat = coordinates[0][1]
    upper_long = coordinates[1][0]
    upper_lat = coordinates[2][1]
    random_long = random.random() * (upper_long - lower_long) + lower_long
    random_lat = random.random() * (upper_lat - lower_lat) + lower_lat
    return [random_long, random_lat]


def build_connection_string():
    """
    Creates the connection string to access the MongoDB database
    """
    load_dotenv()
    return 'mongodb+srv://' + os.getenv('MONGO_USERNAME') + ':' + os.getenv(
        'MONGO_PASSWORD') + '@sohams2cluster-upcyf.mongodb.net/test?retryWrites=true&w=majority'
