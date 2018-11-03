from django.urls import path
from . import controllers

urlpatterns = [
    # path('<str:tweet_id'),
    path('create', controllers.create_tweet),
    path('<str:tweet_id>', controllers.handle_tweet),
    path('emotion/<str:tweet_id>', controllers.handle_emotion),
    path('retweet/<str:tweet_id>', controllers.handle_retweet),
]
