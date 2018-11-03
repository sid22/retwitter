from django.urls import path

from . import controllers

urlpatterns = [
    path('login', controllers.user_login, name='login'),
    path('logout', controllers.user_logout, name='logout'),
    path('signup', controllers.user_signup, name='signup'),
    path('follow', controllers.user_follow, name='follow'),
    path('unfollow', controllers.user_unfollow, name='unfollow')

    # path('admin/', admin.site.urls),
]
