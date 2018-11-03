from django.urls import path
from . import controllers

urlpatterns = [
    # path('<str:tweet_id'),
    path('create', controllers.create_tweet, name='create'),
    path('<str:tweet_id>', controllers.handle_tweet, name='handle'),
    path('emotion/<str:tweet_id>', controllers.handle_emotion, name='emotion'),
    path('retweet/<str:tweet_id>', controllers.handle_retweet, name='retweet'),
]
