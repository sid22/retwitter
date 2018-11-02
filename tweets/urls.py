from django.urls import path
from . import controllers

urlpatterns = [
    path('<str:tweet_id'),
    path('create', controllers.user_login),
    path('delete/<str:tweet_id', controllers.user_logout),
    path('like/<str:tweet_id', controllers.user_signup),
    path('unlike/<str:tweet_id', controllers.user_signup),
    path('retweet/<str:tweet_id', controllers.user_signup),
]
