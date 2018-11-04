import datetime
import uuid

from django.conf import settings

from account.utils.custom_exceptions import (EmptyException, NotAuthorized,
                                             TweetNotFound)


class TweetAll:
    def __init__(self):
        self.db = settings.DB
        # self.r_cache = settings.R_CACHE
        # self.jwt_secret = settings.JWT_SECRET

    def create(self, user_id, tweet_text):
        res = {}
        try:
            if tweet_text == '':
                raise EmptyException("Tweet tex=t")
            new_tweet = {
                "_id": str(uuid.uuid4()),
                "user_id": user_id,
                "tweet_text": tweet_text[:140],
                "created_at": datetime.datetime.utcnow(),
                "fav_count": 0,
                "fav_list": [],
                "retweet_count": 0,
                "retweet_list": [],
                "retweet_user_list": [],
                "is_retweet": False,
                "before_retweet_user": None,
                "before_tweet_id": None,
                "is_reply": False,
                "replies": [],
                "replies_count": 0,
                "is_threaded": False,
                "thread_id": None,
            }
            inserted_tweet = self.db.tweets.insert_one(new_tweet)
            res['message'] = {"Success": "Tweet created succesfully!", "tweet_id": inserted_tweet.inserted_id}
            res['code'] = 200
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def delete(self, user_id, tweet_id):
        res = {}
        try:
            if tweet_id == '' or None:
                raise EmptyException("tweet id")
            
            to_delete_tweet = self.db.tweets.find_one({"_id": tweet_id})
            if to_delete_tweet['user_id'] != user_id:
                raise NotAuthorized
            if to_delete_tweet["is_retweet"] == True:
                # we need to change the original also
                original_query = {"_id": to_delete_tweet["before_tweet_id"]}
                original_update = {"$pull": { "retweet_list": { "$in": [ tweet_id ] } }, 
                                    "$inc": { "retweet_count": -1 }, 
                                    "$pull": { "retweet_user_list": { "$in": [ user_id ] } }}
                tweet_ori_update = self.db.tweets.update_one(original_query, original_update)
                deleted_tweet = self.db.tweets.delete_one({"_id": tweet_id})    
            elif to_delete_tweet["is_reply"] == True:
                ## we need to change the original also
                original_query = {"_id": to_delete_tweet["before_tweet_id"]}
                original_update = { "$pull": { "replies": { "$in": [ tweet_id ] } }, 
                                    "$inc": { "replies_count": -1 } }
                tweet_ori_update = self.db.tweets.update_one(original_query, original_update)
                deleted_tweet = self.db.tweets.delete_one({"_id": tweet_id})
            else:    
                deleted_tweet = self.db.tweets.delete_one({"_id": tweet_id})
            res['message'] = {"Success": "Tweet deleted succesfully!", "tweet_id": tweet_id}
            res['code'] = 200 
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400
        except NotAuthorized:
            res['message'] = {"Error": "The user can only delete their own tweets/replies"}
            res['code'] = 401    
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res
    
    def view(self, tweet_id):
        res = {}
        try:
            if tweet_id == '' or None:
                raise EmptyException("tweet id")
            tweet_view = self.db.tweets.find_one({"_id": tweet_id})
            res['message'] = {"Success": "Tweet fetched succesfully!", "tweet": tweet_view}
            res['code'] = 200               
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400  
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res
            
    def make_emotion(self, user_id, tweet_id):
        res = {}
        try:
            if tweet_id == '' or None:
                raise EmptyException("tweet id")
            tweet_query = {"_id": tweet_id}
            tweet_data = self.db.tweets.find_one(tweet_query)
            tolike = 1
            for i in tweet_data['fav_list']:
                # here we check, if user has already liked the tweet, if yes he now will unlike the tweet
                if i == user_id:
                    tolike = 0
            if tolike == 1:
                update_query = { "$push": { "fav_list": { "$each": [ user_id ] } }, "$inc": { "fav_count": 1 } }
                update_tweet = self.db.tweets.update_one(tweet_query, update_query, upsert=False)
                res['message'] = {"Success": "Tweet with id " + tweet_id + " liked succesfully by user with id " + user_id }
                res['code'] = 200      
            elif tolike == 0:
                update_query = { "$pull": { "fav_list": { "$in": [ user_id ] } }, "$inc": { "fav_count": -1 } }
                update_tweet = self.db.tweets.update_one(tweet_query, update_query, upsert=False)
                res['message'] = {"Success": "Tweet with id " + tweet_id + " unliked succesfully by user with id " + user_id }
                res['code'] = 200      
            
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400  
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def retweet(self, user_id, tweet_id):
        res = {}
        try:
            if tweet_id == '' or None:
                raise EmptyException("tweet id")
            tweet_query = {"_id": tweet_id}
            original_tweet = self.db.tweets.find_one(tweet_query)
            retweet_tweet = {
                "_id": str(uuid.uuid4()),
                "user_id": user_id,
                "tweet_text": original_tweet['tweet_text'],
                "created_at": datetime.datetime.utcnow(),
                "fav_count": 0,
                "fav_list": [],
                "retweet_count": 0,
                "retweet_list": [],
                "retweet_user_list": [],
                "is_retweet": True,
                "before_retweet_user": original_tweet['user_id'],
                "before_tweet_id": original_tweet["_id"],
                "is_reply": False,
                "replies": [],
                "is_threaded": False,
                "thread_id": None,
            }
            new_tweet = self.db.tweets.insert_one(retweet_tweet)
            update_query = { "$push": { "retweet_list": { "$each": [ retweet_tweet["_id"] ] } }, 
                            "$inc": { "retweet_count": 1 }, 
                            "$push": { "retweet_user_list": { "$each": [ user_id ] } }
                            }
            update_orig_tweet = self.db.tweets.update_one(tweet_query, update_query, upsert=False)
            success_msg = str("Retweet with id " + retweet_tweet["_id"] + " created for tweet with id " + tweet_id + " by user with id " + user_id)
            res['message'] = {"Success": success_msg, "retweet_id": retweet_tweet["_id"] }
            res['code'] = 200      
        
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400  
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def reply(self, user_id, tweet_id, reply_text):
        res = {}
        try:
            if tweet_id == '' or None:
                raise EmptyException("tweet id")
            tweet_query = {"_id": tweet_id}
            original_tweet = self.db.tweets.find_one(tweet_query)
            if original_tweet == None:
                raise TweetNotFound
            reply_obj = {
                "_id": str(uuid.uuid4()),
                "user_id": user_id,
                "tweet_text": reply_text[:140],
                "created_at": datetime.datetime.utcnow(),
                "fav_count": 0,
                "fav_list": [],
                "retweet_count": 0,
                "retweet_list": [],
                "retweet_user_list": [],
                "is_retweet": False,
                "before_retweet_user": None,
                "before_tweet_id": original_tweet["_id"],
                "is_reply": True,
                "replies": [],
                "replies_count": 0,
                "is_threaded": False,
                "thread_id": None,
            }
            new_reply = self.db.tweets.insert_one(reply_obj)
            update_query = { "$push": { "replies": { "$each": [ reply_obj["_id"] ] } }, 
                            "$inc": { "replies_count": 1 } }
            update_orig_tweet = self.db.tweets.update_one(tweet_query, update_query, upsert=False)
            success_msg = str("Reply with id " + reply_obj["_id"] + " created for tweet with id " + tweet_id + " by user with id " + user_id)
            res['message'] = {"Success": success_msg, "reply_id": reply_obj["_id"] }
            res['code'] = 200      
        
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400 
        except TweetNotFound:
            res['message'] = {"Error": "No tweet found with given tweet id, cannot add reply"}
            res['code'] = 400      
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def thread(self, user_id, thread_texts):
        res = {}
        try:
            if len(thread_texts) == 0:
                raise EmptyException("Thread count")
            new_tweets = []
            thread_id = str(uuid.uuid1())
            thread_time = datetime.datetime.utcnow()
            for single_tweet in thread_texts:
                if single_tweet == '':
                    raise EmptyException("Any tweet text")
                else:
                    new_tweet = {
                        "_id": str(uuid.uuid4()),
                        "user_id": user_id,
                        "tweet_text": single_tweet[:140],
                        "created_at": thread_time,
                        "fav_count": 0,
                        "fav_list": [],
                        "retweet_count": 0,
                        "retweet_list": [],
                        "retweet_user_list": [],
                        "is_retweet": False,
                        "before_retweet_user": None,
                        "before_tweet_id": None,
                        "is_reply": False,
                        "replies": [],
                        "replies_count": 0,
                        "is_threaded": True,
                        "thread_id": thread_id,
                    }
                    new_tweets.append(new_tweet)
            inserted_tweets = self.db.tweets.insert_many(new_tweets)
            res['message'] = {"Success": "Thread created succesfully!", "thread_id": thread_id, "tweet_ids": [inserted_tweets.inserted_ids] }
            res['code'] = 200
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res

    def thread_view(self, thread_id):
        res = {}
        try:
            if thread_id == '':
                raise EmptyException("Thread id")
            thread_tweets = list(self.db.tweets.find({"thread_id": thread_id}))
            res['message'] = {"Success": "Thread fetched succesfully!", "thread_id": thread_id, "thread_tweets": [thread_tweets] }
            res['code'] = 200
        except EmptyException as e: 
            res['message'] = {"Error": str(e.message + " cannot be empty")}
            res['code'] = 400
        except Exception as e:
            res['message'] = {"Error": "Some intenal error occured try again"}
            res['code'] = 500
        return res
