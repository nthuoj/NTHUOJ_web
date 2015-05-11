#NTHUOJ_WEB
#######Version 1.0.3
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
* python-dev
* mysql-server
* python-pip
* python-mysqldb
* nodejs
* npm
* libjpeg
* bower
* django1.7
* django-bower
* django-axes
* django-autocomplete-light
* django-datetime-widget
* django-bootstrap
* django-bootstrap-form
* requests
* django-ckeditor
* pillow

###Installation:
* Install dependencies (for ubuntu)
```
apt-get install mysql-server
apt-get install python-pip
apt-get install python-mysqldb
apt-get install nodejs
apt-get install npm
apt-get install python-dev
apt-get install libjpeg-dev
npm install -g bower
ln -s /usr/bin/nodejs /usr/bin/node
pip install django==1.7
pip install django-bower
pip install django-axes
pip install django-autocomplete-light
pip install django-datetime-widget
pip install django-bootstrap
pip install django-bootstrap-form
pip install requests
pip install django-ckeditor
pip install -I pillow
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

