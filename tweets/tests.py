# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
# import unittest
from datetime import datetime

from django.test import Client
import unittest
from django.urls import reverse
from jwt import ExpiredSignatureError
from account.helpers.user_auth import UserAuth
from tweets.helpers.tweet_logic import TweetAll
from unittest.mock import patch
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
        Test the login route
        '''
        mock_delete.return_value = self.res
        mock_view.return_value = self.res
        mock_auth.return_value = self.auth_res
        res1 = self.client.get(reverse('handle', kwargs={"tweet_id":"asdas"}))
        res2 = self.client.delete(reverse('handle', kwargs={"tweet_id":"asdas"}))
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

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
        print("\n Starting Tweet API tests...\n")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        print("Finished Tweet API tests...\n")

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

    # @patch('pymongo.collection.Collection.find_one')
    # @patch('pymongo.collection.Collection.delete_one')
    # def test_04_emotion(self, mocked_delete, mocked_find):
    #     user_id = 'abcd'
    #     tweet_id = ['', 'not']
    #     mocked_find.return_value = {
    #         "_id": "abcd",
    #         "is_retweet": False
    #     }
    #     mocked_delete.return_value = 'asa'
    #     res1 = self.tweet_all.view(user_id, tweet_id[0])
    #     res2 = self.tweet_all.view(user_id, tweet_id[1])
    #     self.assertEqual(res1['code'], 400)
    #     self.assertEqual(res2['code'], 200)
