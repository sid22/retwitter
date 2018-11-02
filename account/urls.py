from django.urls import path

from . import controllers

urlpatterns = [
    path('login', controllers.user_login),
    path('logout', controllers.user_logout),
    path('signup', controllers.user_signup),
    path('follow', controllers.user_follow),
    path('unfollow', controllers.user_unfollow)

    # path('admin/', admin.site.urls),
]
