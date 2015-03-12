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

import os

def write_ini_file(host, db, user, pwd):
    ini_file = open('nthuoj.ini', 'w')
    ini_file.write('[client]\n')
    ini_file.write('host = %s\n' % host)
    ini_file.write('database = %s\n' % db)
    ini_file.write('user = %s\n' % user)
    ini_file.write('password = %s\n' % pwd)
    ini_file.write('default-character-set = utf8\n')
    ini_file.close()

def write_email_file(user, pwd):
    email_file = open('emailInfo.py', 'w') 
    email_file.write('EMAIL_HOST_USER = \'%s\'\n' % user)
    email_file.write('EMAIL_HOST_PASSWORD = \'%s\'\n' % pwd)
    email_file.close()

def django_manage(args):
    cmd = 'python ./manage.py ' + args
    os.system(cmd)

def db_migrate():
    apps = ['index', 'problem', 'users', 'contest', 'team', 'group']
    for app in apps:
        django_manage('makemigrations ' + app)
    django_manage('migrate')

