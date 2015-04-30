#NTHUOJ_WEB
=======

##License
---
Please refer to MIT license with [our license file](https://github.com/bruce3557/NTHUOJ_web/blob/master/LICENSE).

##Install Guide
---

###Get our project
```
git clone git@github.com:bruce3557/NTHUOJ_web.git
```

####Dependencies:
* python2.7
* mysql-server
* python-pip
* python-mysqldb
* nodejs
* npm
* bower
* django1.7
* django-bower
* django-axes
* django-autocomplete-light
* django-datetime-widget
* django-bootstrap
* requests

###Installation:
* Install dependencies
```
apt-get install mysql-server
apt-get install python-pip
apt-get install python-mysqldb
apt-get install nodejs
apt-get install npm
npm install -g bower
pip install django-bower
pip install django
pip install django-bower
pip install django-axes
pip install django-autocomplete-light
pip install django-datetime-widget
pip install django-bootstrap
pip install requests
```
* Execute install.py for initial setting.
    ```
    python install.py
    ```

* After installing, you can modify `'project_root/config/nthuoj.cfg'` if your want to change project configurations.

###Email host:
* The email host should be gmail.

* Your google account seeting 'Access for less secure apps' should turn on.

###Virtual judge account
* We use [virtual judge](http://vjudge.net) for judging codes from other resources(UVA, ICPC, etc).

