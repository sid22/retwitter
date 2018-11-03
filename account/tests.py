# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
# import unittest
from datetime import datetime

from django.test import Client
import unittest
from django.urls import reverse
from jwt import ExpiredSignatureError
from account.utils.custom_exceptions import *
from account.helpers.user_auth import UserAuth
from unittest.mock import patch


class APITests(unittest.TestCase):
    '''
    Testing the controller functions only
    '''
    @classmethod
    def setUpClass(self):
        self.client = Client()
        # print("\n" + '\x1b[0;34;40m' + 'Starting API tests...' + '\x1b[0m')
        print("\n Starting API tests...\n")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        print("Finished API tests...\n")

    def test_01_app_basepage(self):
        '''
        Tests the general response codes for routes, defined and notdefined
        '''
        res1 = self.client.get('/')
        self.assertEqual(res1.status_code, 200)

    def test_02_app_user_login(self):
        '''
        Test the login route
        '''
        res1 = self.client.get(reverse('login'))
        res2 = self.client.post(reverse('login'))
        self.assertEqual(res1.status_code, 405)
        self.assertEqual(res2.status_code, 400)

class HandlerTests(unittest.TestCase):
    '''
    Testing the controller functions only
    '''
    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.auser = UserAuth()
        self.valid_sample_user = {"_id": "07d0bdae-0393-4a50-b575-d9245efcf8cf", "password": "7bf4fb3f97cd903a9af16ba419a1a3947ffa293371e2bcb1b868ee6e4baf3aec"}
        self.invalid_sample_user = {"_id": "07d0b-d9245efcf8cf", "password": "7bf4fb3f99a1a3947ffa293371e2bcb1b868ee6e4baf3aec"}
        self.valid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDM3ODIyNDIsInVzZXJfZHQiOiIwN2QwYmRhZTAzOTM0YTUwYjU3NWQ5MjQ1ZWZjZjhjZiJ9.i2VQ6dGj2Ywh3x6TP3zpbFpckNfPzVfXWOYB_xqmrzc"
        # print("\n" + '\x1b[0;34;40m' + 'Starting API tests...' + '\x1b[0m')
        print("\n Starting Handler tests...\n")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        print("Finished Handler tests...\n")

    @patch('pymongo.collection.Collection.count')
    @patch('pymongo.collection.Collection.insert_one')
    @patch('redis.StrictRedis.set')
    def test_01_signup(self, redisset, mocked_insertone, mocked_count):
        '''
        Tests the general response codes for routes, defined and notdefined
        '''
        mocked_count.side_effect = [0, 1, 1, 1, 1]
        username = ["siddharth", '', "siddharth", '']
        password = ["siddharth", "siddharth", '', '']
        res1 = self.auser.signup(username[0], password[0])
        res2 = self.auser.signup(username[1], password[1])
        res3 = self.auser.signup(username[2], password[2])
        res4 = self.auser.signup(username[3], password[3])
        res5 = self.auser.signup(username[0], password[0])
        self.assertEqual(res1['code'], 200)
        self.assertEqual(res2['code'], 400)
        self.assertEqual(res3['code'], 400)
        self.assertEqual(res4['code'], 400)
        self.assertEqual(res5['code'], 409)
    
    @patch('pymongo.collection.Collection.find_one')
    @patch('redis.StrictRedis.set')
    def test_02_login(self, redisset, mocked_findone):
        mocked_findone.side_effect = [self.valid_sample_user, None, None, None, None, self.invalid_sample_user, self.invalid_sample_user]
        username = ["siddharth", '', "siddharth", '']
        password = ["siddharth", "siddharth", '', '']
        res1 = self.auser.login(username[0], password[0])
        res2 = self.auser.login(username[1], password[1])
        res3 = self.auser.login(username[2], password[2])
        res4 = self.auser.login(username[3], password[3])
        res5 = self.auser.login(username[0], password[0])
        self.assertEqual(res1['code'], 200)
        self.assertEqual(res2['code'], 400)
        self.assertEqual(res3['code'], 400)
        self.assertEqual(res4['code'], 400)
        self.assertEqual(res5['code'], 401)
    
    @patch('redis.StrictRedis.get')
    def test_03_chech_auth(self, redisget):
        auth_token = [None, 'abc', self.valid_token]
        redisget.side_effect = [None, None, 'abc', self.valid_token]
        res1 = self.auser.check_auth(auth_token[0])
        res2 = self.auser.check_auth(auth_token[1])
        res3 = self.auser.check_auth(auth_token[1])
        res4 = self.auser.check_auth(auth_token[2])
        self.assertEqual(res1['code'], 400)
        self.assertEqual(res2['code'], 401)
        self.assertEqual(res3['code'], 401)
        self.assertEqual(res4['code'], 200)

    # def test_02_app_user_login(self):
    #     '''
    #     Test the login route
    #     '''
    #     res1 = self.client.get(reverse('login'))
    #     res2 = self.client.post(reverse('login'))
    #     self.assertEqual(res1.status_code, 405)
    #     self.assertEqual(res2.status_code, 400)
        