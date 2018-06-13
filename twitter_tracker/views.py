# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.views.generic import TemplateView
from tweepy import TweepError

from twitter_test import settings
from twitter_test.settings import DEFAULT_ACCOUNT
from twitter_tracker.models import CachedData
from twitter_tracker.utils import collect_twitter_data


class TwitterView(TemplateView):
    template_name = 'twitter_view.html'

    def get_context_data(self, **kwargs):
        default_handle = DEFAULT_ACCOUNT
        handle = None
        count = 10

        if self.request.method == "GET":
            if 'handle' in self.request.GET.keys():
                handle = self.request.GET['handle']
            if 'count' in self.request.GET.keys():
                try:
                    count = int(self.request.GET['count'])
                except ValueError:
                    # count not a valid integer so referring to default count
                    pass
        try:
            if handle is not None:
                cached_data = CachedData.objects.get(handle=handle, timeout__gt=datetime.datetime.now())
            else:
                cached_data = CachedData.objects.get(handle=default_handle, timeout__gt=datetime.datetime.now())
                handle = default_handle

            tweet_data = cached_data.data
        except CachedData.DoesNotExist:
            tweet_data = None
            if handle is not None:
                try:
                    tweet_data = collect_twitter_data(handle, count)
                except TweepError:
                    # handle that has been given is non existent so use the default handle
                    pass
            if tweet_data is None:
                tweet_data = collect_twitter_data(default_handle, count)
                handle = default_handle
            CachedData.objects.filter(handle=handle).delete()

            # cache tweets to stop user requests triggering the twitter api rate limit
            delay = datetime.datetime.now() + datetime.timedelta(seconds=5)
            cache = CachedData(handle=handle, data=tweet_data, timeout=delay)
            cache.save()

        context = super(TwitterView, self).get_context_data(**kwargs)

        context['status_data'] = tweet_data
        context['handle'] = handle
        context['map_api_key'] = settings.GOOGLE_MAP_API
        return context
