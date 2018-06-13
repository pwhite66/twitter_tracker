from django.conf.urls import url

from twitter_tracker.views import TwitterView

urlpatterns = [
    url(r'^$', TwitterView.as_view(), name='twitter_view'),
]