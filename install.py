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
import getpass
import ConfigParser

from func import *


CONFIG_PATH = 'nthuoj/config/nthuoj.cfg'

if not os.path.isfile(CONFIG_PATH):
    # If the config file does not exist, write default config
    write_default_config(CONFIG_PATH)

config = ConfigParser.RawConfigParser()
config.optionxform = str
config.read(CONFIG_PATH)


if not config.has_section('client'):
    # Setting mysql info
    write_config(config, 'client',
        {'default-character-set': 'utf8'},
        host=raw_input('Mysql host: '),
        database=raw_input('Mysql database: '),
        user=raw_input('Mysql user: '),
        password=getpass.getpass('Mysql user password: ')
    )

if not config.has_section('system_version'):
    # Getting system version info
    write_config(config, 'system_version',
        backend=raw_input('Host os version: '),
        gcc=raw_input('gcc version: '),
        gpp=raw_input('g++ version: ')
    )

if not config.has_section('email'):
    # Setting email info
    write_config(config, 'email',
        user=raw_input('Email host(gmail): '),
        password=getpass.getpass("Email host's password: ")
    )

if not config.has_section('vjudge'):
    # Setting virtual judge info
    print 'We use virtual judge(http://vjudge.net) for other judge source(UVA, ICPC, etc.)'
    write_config(config, 'vjudge',
        username=raw_input('Virtual judge username: '),
        password=getpass.getpass("Virtual judge password: ")
    )

# Change defaut path
paths = dict(config.items('path'))
print 'Default path configuration is:\n'
for key in paths:
    print '%s: %s' % (key, paths[key])

if prompt('Customize source code, testcase path?'):
    for key in paths:
        path = raw_input('%s: ' % key)
        paths[key] = path
        os.system('mkdir %s' % path)

    write_config(config, paths)

# Writing our configuration file
with open(CONFIG_PATH, 'wb') as configfile:
    config.write(configfile)

# Bower
if prompt('Install static file by `bower install`?'):
    django_manage('bower install')

# Database Migratinos
django_manage('syncdb')

django_manage('makemigrations')
django_manage('migrate')
