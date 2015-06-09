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
* django-datetime-widget
* django-bootstrap
* django-bootstrap-form
* requests
<<<<<<< HEAD
* git
=======
* django-ckeditor
* pillow
>>>>>>> 04ed9d91f0d50415114330044ea6b41f28054337

###Installation:
* Install dependencies (for ubuntu)
```
<<<<<<< HEAD
sudo apt-get install mysql-server
sudo apt-get install python-pip
sudo apt-get install python-mysqldb
sudo apt-get install nodejs
sudo apt-get install npm
sudo npm install -g bower
sudo ln -s /usr/bin/nodejs /usr/bin/node
sudo pip install django==1.7
sudo pip install django-bower
sudo pip install django-axes
sudo pip install django-autocomplete-light
sudo pip install django-datetime-widget
sudo pip install django-bootstrap
sudo pip install django-bootstrap-form
sudo pip install requests
sudo apt-get install git
=======
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
pip install pillow
>>>>>>> 04ed9d91f0d50415114330044ea6b41f28054337
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
