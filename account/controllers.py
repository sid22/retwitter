from django.http import JsonResponse

from account.helpers.user_auth import UserAuth

user_auth = UserAuth()


def hello_page(request):
    '''
    Param: request
    Controller to hello world
    '''
    message = {
        "Success": "This is the assignment I made for Postman Internship task",
        "person": "Siddharth Goyal"
    }
    response = JsonResponse(message)
    response.status_code = 200
    return response


def user_login(request):
    '''
    Param: request
    Controller to handle login only POST request.
    '''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        res = user_auth.login(username, password)
    elif request.method == 'GET':
        res = {}
        res['message'] = {"Error": "Login resource is for POST request only"}
        res['code'] = 405

    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response


def user_signup(request):
    '''
    Param: request
    Controller to handle signup, only POST request.
    '''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        res = user_auth.signup(username, password)
    elif request.method == 'GET':
        res = {}
        res['message'] = {"Error": "Signup resource is for POST request only"}
        res['code'] = 405

    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response


def user_logout(request):
    '''
    Param: request
    Controller to handle login only POST/GET request.
    '''
    auth_token = request.META.get('HTTP_AUTHORIZATION', '')
    res = user_auth.logout(auth_token)
    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response


def user_follow(request):
    '''
    Param: request
    Controller to handle follow, only POST request.
    '''
    if request.method == 'POST':
        auth_token = request.META.get('HTTP_AUTHORIZATION', '')
        res = user_auth.check_auth(auth_token)
        if res['code'] == 200:
            follow_name = request.POST.get('follow_name', '')
            res = user_auth.follow(res['user_id'], follow_name)

    elif request.method == 'GET':
        res = {}
        res['message'] = {"Error": "Follow resource is for POST request only"}
        res['code'] = 405

    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response


def user_unfollow(request):
    '''
    Param: request
    Controller to handle unfollow, only POST request.
    '''
    if request.method == 'POST':
        auth_token = request.META.get('HTTP_AUTHORIZATION', '')
        res = user_auth.check_auth(auth_token)
        if res['code'] == 200:
            unfollow_name = request.POST.get('unfollow_name', '')
            res = user_auth.unfollow(res['user_id'], unfollow_name)

    elif request.method == 'GET':
        res = {}
        res['message'] = {"Error": "Unfollow resource is for POST request only"}
        res['code'] = 405

    response = JsonResponse(res['message'])
    response.status_code = res['code']
    return response
