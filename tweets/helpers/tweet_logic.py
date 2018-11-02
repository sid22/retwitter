from django.conf import settings

class TweetAll:
    def __init__(self):
        self.db = settings.DB
        self.r_cache = settings.R_CACHE
        self.jwt_secret = settings.JWT_SECRET