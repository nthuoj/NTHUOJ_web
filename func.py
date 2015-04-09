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


def write_mysql_client_config(config, host, db, user, pwd):
    config.add_section('client')
    config.set('client', 'host', host)
    config.set('client', 'database', db)
    config.set('client', 'user', user)
    config.set('client', 'password', pwd)
    config.set('client', 'default-character-set', 'utf8')


def write_email_config(config, user, pwd):
    config.add_section('email')
    config.set('email', 'user', user)
    config.set('email', 'password', pwd)


def write_path_config(config, paths):
    for key in paths:
        config.set('path', key, paths[key])


def django_manage(args):
    cmd = 'python ./manage.py ' + args
    os.system(cmd)

