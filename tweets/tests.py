# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
# import unittest
from unittest.mock import patch

from django.test import Client
from django.urls import reverse

from account.helpers.user_auth import UserAuth
from tweets.helpers.tweet_logic import TweetAll

from .test_helpers import InsertResult


# Create your tests here.
class TweetAPITests(unittest.TestCase):
    '''
    Testing the controller functions only
    '''
    @classmethod
    def setUpClass(self):
        res = {}
        res['message'] = {"Success": "mocking"}
        res['code'] = 200
        auth_res = {}
        auth_res['code'] = 200
        auth_res['user_id'] = 'someid'
        self.client = Client()
        self.res = res
        self.auth_res = auth_res
        # print("\n" + '\x1b[0;34;40m' + 'Starting API tests...' + '\x1b[0m')
        print("\n Starting Tweet API tests...\n")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        print("Finished Tweet API tests...\n")

    @patch('account.helpers.user_auth.UserAuth.check_auth')
    @patch('tweets.helpers.tweet_logic.TweetAll.create')
    def test_01_create_tweet(self, mock_create, mock_auth):
        '''
        Test the login route
        '''
        mock_create.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('create'))
        res2 = self.client.post(reverse('create'))
        self.assertEqual(res1.status_code, 405)
        self.assertEqual(res2.status_code, 200)

    @patch('account.helpers.user_auth.UserAuth.check_auth')
    @patch('tweets.helpers.tweet_logic.TweetAll.make_emotion')
    def test_02_emotion_tweet(self, mock_emotion, mock_auth):
        '''
        Test the login route
        '''
        mock_emotion.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('emotion', kwargs={"tweet_id":"asdas"}))
        res2 = self.client.post(reverse('emotion', kwargs={"tweet_id":"asdas"}))
        self.assertEqual(res1.status_code, 405)
        self.assertEqual(res2.status_code, 200)

    @patch('account.helpers.user_auth.UserAuth.check_auth')
    @patch('tweets.helpers.tweet_logic.TweetAll.retweet')
    def test_03_retweet_tweet(self, mock_retweet, mock_auth):
        '''
        Test the login route
        '''
        mock_retweet.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('retweet', kwargs={"tweet_id":"asdas"}))
        res2 = self.client.post(reverse('retweet', kwargs={"tweet_id":"asdas"}))
        self.assertEqual(res1.status_code, 405)
        self.assertEqual(res2.status_code, 200)

    @patch('account.helpers.user_auth.UserAuth.check_auth')
    @patch('tweets.helpers.tweet_logic.TweetAll.delete')
    @patch('tweets.helpers.tweet_logic.TweetAll.view')
    def test_04_handle_tweet(self, mock_view, mock_delete, mock_auth):
        '''
        Test the handle view/delete route
        '''
        mock_delete.return_value = self.res
        mock_view.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('handle', kwargs={"tweet_id":"asdas"}))
        res2 = self.client.delete(reverse('handle', kwargs={"tweet_id":"asdas"}))
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

    @patch('account.helpers.user_auth.UserAuth.check_auth')
    @patch('tweets.helpers.tweet_logic.TweetAll.reply')
    def test_05_handle_reply(self, mock_reply, mock_auth):
        '''
        Test the reply route
        '''
        mock_reply.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('reply', kwargs={"tweet_id":"asdas"}))
        res2 = self.client.post(reverse('reply', kwargs={"tweet_id":"asdas"}))
        self.assertEqual(res1.status_code, 405)
        self.assertEqual(res2.status_code, 200)

    @patch('account.helpers.user_auth.UserAuth.check_auth')
    @patch('tweets.helpers.tweet_logic.TweetAll.thread')
    def test_05_handle_thread(self, mock_thread, mock_auth):
        '''
        Test the thread route
        '''
        mock_thread.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('thread'))
        res2 = self.client.post(reverse('thread'))
        self.assertEqual(res1.status_code, 400)
        self.assertEqual(res2.status_code, 200)
    
    @patch('account.helpers.user_auth.UserAuth.check_auth')
    @patch('tweets.helpers.tweet_logic.TweetAll.thread')
    def test_06_view_thread(self, mock_thread, mock_auth):
        '''
        Test the thread route
        '''
        mock_thread.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('view_thread', kwargs={"thread_id":"asdas"}))
        self.assertEqual(res1.status_code, 200)

class TweetHandlerTests(unittest.TestCase):
    '''
    Testing the controller functions only
    '''
    @classmethod
    def setUpClass(self):
        res = {}
        res['message'] = {"Success": "mocking"}
        res['code'] = 200
        auth_res = {}
        auth_res['code'] = 200
        auth_res['user_id'] = 'someid'
        self.client = Client()
        self.res = res
        self.auth_res = auth_res
        self.tweet_all = TweetAll()
        # print("\n" + '\x1b[0;34;40m' + 'Starting API tests...' + '\x1b[0m')
        print("\n Starting Tweet Handler tests...\n")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        print("Finished Tweet Handler tests...\n")

    @patch('pymongo.collection.Collection.insert_one')
    def test_01_create(self, mocked_insert):
        user_id = 'abcd'
        tweet_text = ['', 'not']
        ins = InsertResult()
        mocked_insert.return_value = ins
        res1 = self.tweet_all.create(user_id, tweet_text[0])
        res2 = self.tweet_all.create(user_id, tweet_text[1])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res1['code'], 400)

    @patch('pymongo.collection.Collection.find_one')
    @patch('pymongo.collection.Collection.delete_one')
    def test_02_delete(self, mocked_delete, mocked_find):
        user_id = 'abcd'
        tweet_id = ['', 'not']
        mocked_find.return_value = {
            "_id": "abcd",
            "is_retweet": False
        }
        mocked_delete.return_value = 'asa'
        res1 = self.tweet_all.delete(user_id, tweet_id[0])
        res2 = self.tweet_all.delete(user_id, tweet_id[1])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 200)
    
    @patch('pymongo.collection.Collection.find_one')
    @patch('pymongo.collection.Collection.delete_one')
    def test_03_view(self, mocked_delete, mocked_find):
        user_id = 'abcd'
        tweet_id = ['', 'not']
        mocked_find.return_value = {
            "_id": "abcd",
            "is_retweet": False
        }
        mocked_delete.return_value = 'asa'
        res1 = self.tweet_all.view(user_id, tweet_id[0])
        res2 = self.tweet_all.view(user_id, tweet_id[1])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 200)

    @patch('pymongo.collection.Collection.find_one')
    @patch('pymongo.collection.Collection.update_one')
    def test_04_emotion(self, mocked_update, mocked_find):
        user_id = "abcd"
        tweet_id = ["", "not"]
        mocked_find.return_value = {
            "_id": "abcd",
            "fav_list": [ ]
        }
        mocked_update.return_value = 'asa'
        res1 = self.tweet_all.make_emotion(user_id, tweet_id[0])
        res2 = self.tweet_all.make_emotion(user_id, tweet_id[1])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 200)

    @patch('pymongo.collection.Collection.find_one')
    @patch('pymongo.collection.Collection.insert_one')
    @patch('pymongo.collection.Collection.update_one')
    def test_05_retweet(self, mocked_update, mocked_insert, mocked_find):
        user_id = 'abcd'
        tweet_id = ['', 'not']
        mocked_find.return_value = {
            "_id": "abcd",
            "is_retweet": False,
            "fav_list": [],
            "user_id": 'mock_id',
            "tweet_text": "mock"
        }
        mocked_insert.return_value = 'asa'
        mocked_update.return_value = 'asa'
        res1 = self.tweet_all.retweet(user_id, tweet_id[0])
        res2 = self.tweet_all.retweet(user_id, tweet_id[1])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 200)

    @patch('pymongo.collection.Collection.find_one')
    @patch('pymongo.collection.Collection.insert_one')
    @patch('pymongo.collection.Collection.update_one')
    def test_06_reply(self, mocked_update, mocked_insert, mocked_find):
        user_id = 'abcd'
        tweet_id = ['', 'not']
        mocked_find.return_value = {
            "_id": "abcd",
            "is_retweet": False,
            "fav_list": [],
            "user_id": 'mock_id',
            "tweet_text": "mock"
        }
        mocked_insert.return_value = 'asa'
        mocked_update.return_value = 'asa'
        reply_text = "reply"
        res1 = self.tweet_all.reply(user_id, tweet_id[0], reply_text)
        res2 = self.tweet_all.reply(user_id, tweet_id[1], reply_text)
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 200)

    @patch('pymongo.collection.Collection.insert_many')
    def test_07_thread(self, mocked_insert):
        user_id = 'abcd'
        tweet_id = ['', 'not']
        ins = InsertResult()
        mocked_insert.return_value = ins
        thread_texts = [[], ["thread"]]
        res1 = self.tweet_all.thread(user_id, thread_texts[0])
        res2 = self.tweet_all.thread(user_id, thread_texts[1])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 200)

    @patch('pymongo.collection.Collection.find')
    def test_08_thread_view(self, mocked_find):
        thread_id = ['', 'not']
        mocked_find.return_value = {}
        res1 = self.tweet_all.thread_view(thread_id[0])
        res2 = self.tweet_all.thread_view(thread_id[1])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 200)
