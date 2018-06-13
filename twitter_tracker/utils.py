import tweepy
from tweepy import OAuthHandler

from twitter_test.settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, \
    TWITTER_ACCESS_SECRET
from twitter_tracker.models import Location


def collect_twitter_data(username, count):
    """
    gets the most recent messages from a users timeline
    :param username: twitter handle
    :param count: maximum number of tweets to return
    :return: [{'text': message in the tweet 'location': generalized location data or None},]
    """


    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

    api = tweepy.API(auth)

    status_list = []
    for status in api.user_timeline(username, count=count):
        status_dict = {'text': status.text, 'location': None}
        if status.place is not None:
            try:
                status_dict['location'] = Location.objects.get(iso_code=status.place.country_code)
            except Location.DoesNotExist:
                pass
        status_list.append(status_dict)
    return status_list
