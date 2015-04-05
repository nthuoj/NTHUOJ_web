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
import ConfigParser

from func import *

CONFIG_PATH = 'nthuoj/config/nthuoj.cfg'

config = ConfigParser.RawConfigParser()
config.optionxform = str
config.read(CONFIG_PATH)


if not config.has_section('client'):
    # Setting mysql info
    host = raw_input('Mysql host: ')
    db = raw_input('Mysql database: ')
    user = raw_input('Mysql user: ')
    pwd = getpass.getpass()
    write_mysql_client_config(config, host, db, user, pwd)
    print '========================================'

if not config.has_section('email'):
    # Setting email info
    email_host = raw_input('Email host(gmail): ')
    email_host_pwd = getpass.getpass("Email host's password : ")
    write_email_config(config, email_host, email_host_pwd)
    print '========================================'

# Change defaut path
paths = dict(config.items('path'))
print 'Default path configuration is:\n'
for key in paths:
    print '%s: %s' % (key, paths[key])
ans = raw_input('\nCustomize source code, testcase path? [Y/n] ')
if ans == '' or ans == 'y' or ans == 'Y':
    for key in paths:
        path = raw_input('%s: ' % key)
        paths[key] = path
        os.system('mkdir %s' % path)

    write_path_config(config, paths)
    print '========================================'

# Writing our configuration file
with open(CONFIG_PATH, 'wb') as configfile:
    config.write(configfile)

# Create super user
ans = raw_input('Create super user?[Y/n] ')
if ans == '' or ans == 'y' or ans == 'Y':
    django_manage('createsuperuser')

# Database Migratinos
django_manage('syncdb')
django_manage('makemigrations')
django_manage('migrate')
