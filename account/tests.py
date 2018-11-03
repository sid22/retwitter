# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
# import unittest
from datetime import datetime

from django.test import Client
import unittest
from django.urls import reverse
from jwt import ExpiredSignatureError

from unittest.mock import patch


class APITests(unittest.TestCase):
    '''
    Testing the controller functions only
    '''
    @classmethod
    def setUpClass(cls):
        # print("\n" + '\x1b[0;34;40m' + 'Starting API tests...' + '\x1b[0m')
        print("\n Starting API tests...\n")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print("Finished API tests...\n")

    def test_01_app_health(self):
        '''
        Tests the general response codes for routes, defined and notdefined
        '''
        client = Client()
        res1 = client.get('/')
        self.assertEqual(res1.status_code, 200)

    # @patch('appauth.handlers.handlers.UserAuth.login')
    # def test_02_api_auth(self, mocked_login):
    #     '''
    #     Testing login controller, we mock the login function
    #     '''
    #     mocked_login.return_value = ({
    #         'error': {
    #             'status': 'Failure',
    #             'message': 'User Not Found',
    #             'code': -3
    #             }
    #         }, 400)
    #     client = RequestsClient()
    #     res1 = client.post('http://localhost:8000/user/auth/', data={
    #         'username': 'thistestemailnotexist@innovaccer.com',
    #         'password': 'test'
    #     })
    #     res2 = client.post('http://localhost:8000/user/auth/', data={
    #         'username': '',
    #         'password': ''
    #     })
    #     res3 = client.post('http://localhost:8000/user/auth/', data={
    #     })
    #     res4 = client.get("http://localhost:8000/user/auth/")
    #     res5 = client.post('http://localhost:8000/user/auth/', data={
    #         'username': '',
    #         'password': '',
    #         'type': 'ad'
    #     })
    #     res6 = client.post('http://localhost:8000/user/auth/', data={
    #         'username': '',
    #         'password': '',
    #         'type': 'wrongtype'
    #     })
    #     self.assertEqual(res1.status_code, 400)
    #     self.assertEqual(res2.status_code, 422)
    #     self.assertEqual(res3.status_code, 404)
    #     self.assertEqual(res4.status_code, 405)
    #     self.assertEqual(res5.status_code, 422)
    #     self.assertEqual(res6.status_code, 404)

    # @patch('appauth.handlers.handlers.UserAuth.logout')
    # def test_03_api_logout(self, mocked_logout):
    #     mocked_logout.return_value = {
    #         "message": "Success"
    #     }
    #     client = RequestsClient()
    #     headers = {
    #         'Authorization': "Authorization eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjoiMzE2YzI2NmMtNmM3NS00Zjc0LTkwNzAtZGY4YWJmMDNmNTE5IiwiaWF0IjoxNTI4NTc5NTIzLCJsb3V0IjpmYWxzZSwic3ViIjoie1widXNlcl9pZFwiOiBcInVzZXJfMVwiLCBcInJlbW90ZV9hZGRyZXNzXCI6IFwiMTI3LjAuMC4xXCIsIFwiZnVsbF9uYW1lXCI6IFwiSGVhbHRoQ2FyZSwgSW5ub3ZhY2NlciBEXCIsIFwiZW1haWxcIjogXCJjYXJlQGlubm92YWNjZXIuY29tXCJ9IiwiZXhwIjoxNTI4NjY1OTIzfQ.e2U5swaQIKYIwETLtgbkjFQt3p4w4SiBX7mHlfW_L8I"
    #     }
    #     response = client.post('http://localhost:8000/user/logout/', data={})
    #     response2 = client.get('http://localhost:8000/user/logout/', data={})
    #     response3 = client.get('http://localhost:8000/user/logout/', headers=headers)
    #     self.assertEqual(response.status_code, 405)
    #     self.assertEqual(response2.status_code, 400)
    #     self.assertEqual(response3.status_code, 200)

    # @patch('appauth.handlers.handlers.UserAuth.invalidate_adip')
    # def test_04_api_setip(self, mocked_invalidate):
    #     mocked_invalidate.return_value = ('teststring', 200)
    #     client = RequestsClient()
    #     response = client.get('http://localhost:8000/user/setip/')
    #     response2 = client.post('http://localhost:8000/user/setip/', data={
    #         "ip" : ""
    #     })
    #     response3 = client.post('http://localhost:8000/user/setip/', data={})
    #     response4 = client.post('http://localhost:8000/user/setip/', data={
    #         "ip" : "someip"
    #     })
    #     self.assertEqual(response.status_code, 405)
    #     self.assertEqual(response2.status_code, 404)
    #     self.assertEqual(response3.status_code, 404)
    #     self.assertEqual(response4.status_code, 200)
