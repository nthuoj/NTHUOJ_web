#NTHUOJ_WEB
#######Version 1.0.2
=======

##License
---
Please refer to MIT license with [our license file](https://github.com/bruce3557/NTHUOJ_web/blob/master/LICENSE).

##Install Guide
---

###Get our project
```
git clone https://github.com:bruce3557/NTHUOJ_web.git
```

###Configure Git For Installing Bower Dependencies
```
git config --global url."https://".insteadOf git://
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
* django-bootstrap
* django-bootstrap-form
* django-ckeditor
* django-datetime-widget
* requests
* git
* pillow
* dos2unix

###Installation:
* Install dependencies (for ubuntu)
```
sudo apt-get install git
sudo apt-get install mysql-server python-mysqldb
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo apt-get install libjpeg-dev
sudo apt-get install dos2unix
sudo apt-get install npm nodejs
sudo npm install -g bower
sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo pip install -r requirements.txt
```

* Execute install.py for initial setting.
```
python install.py
```
* Please DON'T run this command with sudo to prevent error in permission setttings.
* Information other than those concerning database can be left blank and be configured later by modifying `'project_root/config/nthuoj.cfg'`.
* Our project will not automatically create a database for you. So if you want to use a local database, please create it yourself.


###Email host:
* The email host should be gmail.

* Your google account seeting 'Access for less secure apps' should turn on.
