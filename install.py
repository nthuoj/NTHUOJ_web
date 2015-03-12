'''
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
'''


import getpass
import os.path

from func import *


if not os.path.isfile('nthuoj.ini'):
    # Setting nthuoj.ini
    host = raw_input('Mysql host: ')
    db = raw_input('Mysql database: ')
    user = raw_input('Please input your mysql user: ')
    pwd = getpass.getpass()
    write_ini_file(host, db, user, pwd)

if not os.path.isfile('emailInfo.py'):
    # Setting emailInfo.py
    email_host = raw_input('Email host(gmail): ')
    email_host_pwd = getpass.getpass('Email host\'s password : ')
    write_email_file(email_host, email_host_pwd)

# Database Migratinos
db_migrate()


# Create super user
ans = raw_input('Create super user?[Y/n] ')
if ans == '' or ans == 'y' or ans == 'Y':
    django_manage('createsuperuser')

# Install needed library & setup

# django-axes
django_manage('syncdb')
