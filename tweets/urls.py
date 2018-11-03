from django.urls import path
from . import controllers

urlpatterns = [
    # path('<str:tweet_id'),
    path('create', controllers.create_tweet, name='create'),
    path('thread/', controllers.thread_tweet, name='thread'),
    path('<str:tweet_id>', controllers.handle_tweet, name='handle'),
    path('emotion/<str:tweet_id>', controllers.handle_emotion, name='emotion'),
    path('retweet/<str:tweet_id>', controllers.handle_retweet, name='retweet'),
    path('reply/<str:tweet_id>', controllers.handle_reply, name='reply'),
]
