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

import os

DEFAULT_CONFIG = """
[path]
submission_code_path = /var/nthuoj/code/
testcase_path = /var/nthuoj/testdata/
special_judge_path = /var/nthuoj/specialJudge/
partial_judge_path = /var/nthuoj/partialJudge/

[compiler_option]
C = C: -O2 -lm -std=c99
CPP = C++:  -O2 -lm -std=c++
CPP11 = C++11: -O2 -lm -std=c++11

[file_extension]
C = c
CPP = cpp
CPP11 = cpp

[web_theme]
paper = Paper
cosmo = Cosmo
darkly = Darkly
lumen = Lumen
readable = Readable
simplex = Simplex
spacelab = Spacelab
united = United
cerulean = Cerulean
cyborg = Cyborg
flatly = Flatly
journal = Journal
sandstone = Sandstone
slate = Slate
superhero = Superhero
yeti = Yeti
"""


def write_default_config(path):
    print 'Writing default config...',
    with open(path, 'w') as f:
        f.write(DEFAULT_CONFIG)
    print 'done\n'


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


def write_vjudge_config(config, user, pwd):
    config.add_section('vjudge')
    config.set('vjudge', 'username', user)
    config.set('vjudge', 'password', pwd)

def django_manage(args):
    cmd = 'python ./manage.py ' + args
    os.system(cmd)


def prompt(question):
    """Prompt user's intention (yes or no)"""
    ans = raw_input(question + '[Y/n] ')
    if ans == '' or ans == 'y' or ans == 'Y':
        return True
    return False

