import datetime
import hashlib
import time
import uuid

import jwt
from django.conf import settings

from account.utils.custom_exceptions import (AlreadyFollowingUser,
                                             DuplicateUser, EmptyException,
                                             IncorrectPassword, SessionExpired,
                                             TokenNotPresent, UserNotFound, CannotFollowItself)


class UserAuth:
    def __init__(self):
        self.db = settings.DB
        self.r_cache = settings.R_CACHE
        self.jwt_secret = settings.JWT_SECRET

    def check_auth(self, auth_token):
        res = {}
        try:
            if auth_token == None:
                raise TokenNotPresent
            cache_val = self.r_cache.get(auth_token)
            if cache_val == 0 or cache_val == None:
                raise SessionExpired
            token_val = jwt.decode(auth_token, self.jwt_secret, algorithms=['HS256'])
            concat_id = token_val['user_dt']
            user_id = concat_id[:8] + '-' + concat_id[8:12] + '-' + concat_id[12:16] + '-' + concat_id[16:20] + '-' + concat_id[20:]
            res['message'] = {"Success": "Valid Auth"}
            res['code'] = 200
            res['user_id'] = user_id

        except TokenNotPresent as e:
            res['message'] = e.message
            res['code'] = 400
        except jwt.exceptions.ExpiredSignatureError:
            res['message'] = {"Error": "Please obtain a fresh token by logging in again, you current token has expired"}
            res['code'] = 401
        except SessionExpired:
            res['message'] = {"Error": "Token not valid, please login to get a valid token first"}
            res['code'] = 401
        except jwt.exceptions.InvalidSignatureError:
            res['message'] = {"Error": "Token not valid, please login to get a valid token first"}
            res['code'] = 401    
        except jwt.exceptions.InvalidTokenError:
            res['message'] = {"Error": "Token not valid, please login to get a valid token first"}
            res['code'] = 401
        except Exception:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res  

    def follow(self, user_id, follow_name):
        res = {}
        try:
            query_follower = {"_id": user_id}
            # We can reasonably assume user main exists as this id from token

            user_main = self.db.users.find_one(query_follower)
            if user_main['username'] == follow_name:
                raise CannotFollowItself
            
            for i in user_main['following']:
                if i == follow_name:
                    raise AlreadyFollowingUser
            update_follower = { "$push": { "following": { "$each": [ follow_name ] } }} 
            query_followed = { "username": follow_name }
            update_followed = { "$push": { "followers": { "$each": [ user_main['username'] ] } }} 
         
            followed = self.db.users.update_one(query_followed, update_followed, upsert=False)
            if followed.modified_count != 1:
                raise UserNotFound
            follower = self.db.users.update_one(query_follower, update_follower, upsert=False)
            res['message'] = {"Success": user_main['username'] + " has succesfully unfollowed " + follow_name}
            res['code'] = 200   

        except UserNotFound:
            res['message'] = {"Error": "The user to be followed does not exist"}
            res['code'] = 406   
        except CannotFollowItself:
            res['message'] = {"Error": user_main['username'] + " cannot follow/unfollow itself"}
            res['code'] = 406   
        except AlreadyFollowingUser:
            res['message'] = {"Error": user_main['username'] + " user is already following " + follow_name }
            res['code'] = 406   
        except Exception:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def unfollow(self, user_id, unfollow_name):
        res = {}
        try:
            query_follower = {"_id": user_id}
            # We can reasonably assume user main exists as this id from token

            user_main = self.db.users.find_one(query_follower)
            if user_main['username'] == unfollow_name:
                raise CannotFollowItself
            init_fol = len(user_main['following'])
            user_main['following'].remove(unfollow_name)

            update_follower = { "$pull": { "following": { "$in": [ unfollow_name ] } }} 
            query_followed = { "username": unfollow_name }
            update_followed = { "$pull": { "followers": { "$in": [ user_main['username'] ] } }} 
         
            followed = self.db.users.update_one(query_followed, update_followed, upsert=False)
            if followed.modified_count != 1:
                raise UserNotFound
            follower = self.db.users.update_one(query_follower, update_follower, upsert=False)
            res['message'] = {"Success": user_main['username'] + " has succesfully unfollowed " + unfollow_name}
            res['code'] = 200   

        except UserNotFound:
            res['message'] = {"Error": "The user to be followed does not exist"}
            res['code'] = 406   
        except CannotFollowItself:
            res['message'] = {"Error": user_main['username'] + " cannot follow/unfollow itself"}
            res['code'] = 406   
        except ValueError:
            res['message'] = {"Error": user_main['username'] + " user is not following " + unfollow_name }
            res['code'] = 406       
        except Exception:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def signup(self, username, password):
        res = {}
        try:
            if username == '' or username == None:
                raise EmptyException('Username')
            elif password == '' or password == None:
                raise EmptyException('Password')
            elif username == '' or password == '' or username == None or password == None:
                raise EmptyException('Username and Password')
            duplicate = self.db.users.count({"username": username})
            if duplicate != 0:
                raise DuplicateUser
            ## we can add checks for username/password type/length here

            # salt:-   .join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
            to_insert = {
                "_id": str(uuid.uuid4()),
                "username": username,
                "password": hashlib.sha256(str(password).encode('utf-8')).hexdigest(),
                "date_created": time.time(),
                "followers": [],
                "following": []
            }
            inserted = self.db.users.insert_one(to_insert)
            # u_hash = str(inserted.inserted_id).replace('-','')
            u_hash = to_insert["_id"].replace('-', '')
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
                "user_dt": u_hash
            }
            u_token = jwt.encode(payload, self.jwt_secret, algorithm='HS256').decode('utf-8')
            self.r_cache.set(u_token, datetime.datetime.utcnow())
            res['message'] = {"Success": "User added succesfully!", "token": u_token}
            res['code'] = 200

        except EmptyException as e:
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400
        except DuplicateUser:
            res['message'] = {"Error": "User with same username already exists"}
            res['code'] = 409
        except Exception:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def login(self, username, password):
        res = {}
        try:
            if username == '' or username == None:
                raise EmptyException('Username')
            elif password == '' or password == None:
                raise EmptyException('Password')
            elif username == '' or password == '' or username == None or password == None:
                raise EmptyException('Username and Password')

            user_find = self.db.users.find_one({"username": username})
            if user_find == None:
                raise UserNotFound
            enc_password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
            if user_find['password'] != enc_password:
                raise IncorrectPassword
            
            u_hash = user_find["_id"].replace('-', '')
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
                "user_dt": str(u_hash)
            }
            u_token = jwt.encode(payload, self.jwt_secret, algorithm='HS256').decode('utf-8')
            self.r_cache.set(u_token, datetime.datetime.utcnow())
            res['message'] = {"Success": "User authenticated succesfully!", "token": u_token}
            res['code'] = 200

        except EmptyException as e:
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400
        except UserNotFound:
            res['message'] = {"Error": "No user with provided username found"}
            res['code'] = 401
        except IncorrectPassword:
            res['message'] = {"Error": "Incorrect password"}
            res['code'] = 401    
        except Exception:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def logout(self, auth_token):
        res = {}
        try:
            if auth_token == None:
                raise TokenNotPresent
            r_resp = self.r_cache.delete(auth_token)
            res['message'] = {"Success": "User logged out succesfully!"}
            res['code'] = 200
        except TokenNotPresent as e:
            res['message'] = {"Error": e.message}
            res['code'] = 400
        except Exception:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res  
