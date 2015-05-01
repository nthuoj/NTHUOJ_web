"""
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase

from users.models import User


# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test001', password='test001')
        user.is_active = True
        user.save()

    def test_login(self):
        """Test basic login function"""
        response = self.client.login(username='test001', password='wrong')
        self.assertEqual(response, False)
        response = self.client.login(username='test001', password='test001')
        self.assertEqual(response, True)
        self.client.logout()

    def test_block_wrong_tries(self):
        """Test if the client will be blocked for over 3 wrong tries"""
        # wrong tries for 3 times
        for wrong_tries in range(3):
            response = self.client.post(
                reverse('users:login'),
                {'username': 'test001', 'password': 'wrong'})
            self.assertEqual(response.status_code, 200)

        # get blocked for forth wrong tries
        response = self.client.post(
            reverse('users:login'),
            {'username': 'test001', 'password': 'wrong'})
        self.assertNotEqual(response.status_code, 200)

    def test_sign_up(self):
        """Test if the client is able to sign up"""
        # initial user count
        user_count = User.objects.all().count()

        # sign up with different password confirmation
        self.client.post(
            reverse('users:create'),
            {'username': 'test002', 'password1': 'test002',
            'password2':'002test', 'email': 'oj@nthucs.edu.tw'})
        self.assertNotEqual(User.objects.all().count(), user_count + 1)

        # sign up with invalid email format
        self.client.post(
            reverse('users:create'),
            {'username': 'test002', 'password1': 'test002',
                'password2':'test002', 'email': 'oj'})
        self.assertNotEqual(User.objects.all().count(), user_count + 1)

        # sign up with used username
        self.client.post(
            reverse('users:create'),
            {'username': 'test001', 'password1': 'test002',
            'password2':'test002', 'email': 'oj@nthucs.edu.tw'})
        self.assertNotEqual(User.objects.all().count(), user_count + 1)

