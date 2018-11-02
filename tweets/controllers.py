from django.http import JsonResponse
from account.helpers.user_auth import UserAuth
from tweets.helpers.tweet_logic import TweetAll

user_auth = UserAuth()
tweet = TweetAll()

def create_tweet(request):
    if request.method == 'POST':
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        res = user_auth.check_auth(auth_token) 
        if res['code'] == 200:
            tweet_text = request.POST.get('tweet_text', '')
            res = user_auth.login(es['user_id'], tweet_text)    
    elif request.method == 'GET':
        res = {}
        res['message'] = {"Error": "Create tweet resource is for POST request only"}
        res['code'] = 405

    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response