from django.http import JsonResponse
from account.helpers.user_auth import UserAuth
from tweets.helpers.tweet_logic import TweetAll

user_auth = UserAuth()
tweet = TweetAll()

def create_tweet(request):
    if request.method == 'POST':
        auth_token = request.META.get('HTTP_AUTHORIZATION', '')
        res = user_auth.check_auth(auth_token)
        if res['code'] == 200:
            tweet_text = request.POST.get('tweet_text', '')
            res = tweet.create(res['user_id'], tweet_text)    
    elif request.method == 'GET':
        res = {}
        res['message'] = {"Error": "Create tweet resource is for POST request only"}
        res['code'] = 405

    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response

def handle_tweet(request, tweet_id):
    auth_token = request.META.get('HTTP_AUTHORIZATION', '')
    res = user_auth.check_auth(auth_token)    
    if res['code'] == 200:
        if request.method == 'DELETE':
            res = tweet.delete(res['user_id'], tweet_id)
        if request.method == 'GET':
            res = tweet.view(res['user_id'], tweet_id)
    # if request.method == 'POST':
    #     auth_token = request.META.get('HTTP_AUTHORIZATION')
    #     res = user_auth.check_auth(auth_token)
    #     if res['code'] == 200:
    #         tweet_text = request.POST.get('tweet_text', '')
    #         res = tweet.delete(res['user_id'], tweet_text)    
    # elif request.method == 'GET':
    #     res = {}
    #     res['message'] = {"Error": "Create tweet resource is for POST request only"}
    #     res['code'] = 405

    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response

def handle_emotion(request, tweet_id):
    auth_token = request.META.get('HTTP_AUTHORIZATION', '')
    res = user_auth.check_auth(auth_token)    
    if res['code'] == 200:
        if request.method == 'POST':
            res = tweet.make_emotion(res['user_id'], tweet_id)
        else:
            res = {}
            res['message'] = {"Error": "Create tweet resource is for POST request only"}
            res['code'] = 405
    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response

def handle_retweet(request, tweet_id):
    auth_token = request.META.get('HTTP_AUTHORIZATION', '')
    res = user_auth.check_auth(auth_token)    
    if res['code'] == 200:
        if request.method == 'POST':
            res = tweet.retweet(res['user_id'], tweet_id)
        else:
            res = {}
            res['message'] = {"Error": "Create tweet resource is for POST request only"}
            res['code'] = 405
    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response

def handle_reply(request, tweet_id):
    auth_token = request.META.get('HTTP_AUTHORIZATION', '')
    res = user_auth.check_auth(auth_token)    
    if res['code'] == 200:
        if request.method == 'POST':
            reply_text = request.POST.get('reply_text', '')
            res = tweet.reply(res['user_id'], tweet_id, reply_text)
        else:
            res = {}
            res['message'] = {"Error": "Create tweet resource is for POST request only"}
            res['code'] = 405
    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response

def thread_tweet(request, thread_id=''):
    if request.method == 'POST':
        auth_token = request.META.get('HTTP_AUTHORIZATION', '')
        res = user_auth.check_auth(auth_token)
        if res['code'] == 200:
            thread_count = request.POST.get('thread_count', 0)
            i = 1
            thread_texts = []
            while i < int(thread_count)+1:
                to_get = "tweet_text_" + str(i)
                thread_texts.append(request.POST.get(to_get, ''))
                i = i + 1
            res = tweet.thread(res['user_id'], thread_texts)    
    elif request.method == 'GET':
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        res = user_auth.check_auth(auth_token)
        if res['code'] == 200:
            res = tweet.thread_view(thread_id)    
    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response