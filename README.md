[![Build Status](https://travis-ci.org/henryyang42/NTHUOJ_web.svg)](https://travis-ci.org/henryyang42/NTHUOJ_web)

#NTHUOJ_WEB
#######Version 1.0.4
=======

##License
---
Please refer to MIT license with [our license file](https://github.com/bruce3557/NTHUOJ_web/blob/master/LICENSE).

##Install Guide
---

###Get our project
```
git clone https://github.com/bruce3557/NTHUOJ_web.git
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
* git
* dos2unix
* python dependencies in [requirements.txt](requirements.txt)

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
* For more detailed deployment instructions, you can follow this [note](https://gist.github.com/henryyang42/e70c7f444788e674c4da)

###Email:
* In our project, we use **Postfix** as the mail server for sending emails of registration or resetting password.

* It's recommended that you install our project on a machine which has an IP address or a domain name belongs to NTHU, or outgoing emails would almost definitely be blocked by other mail service providers.

* The mail server will be installed in a docker image, so if you want to enable email sending, you have to build the image first. Please check [here](https://github.com/nthuoj/NTHUOJ_web_docker) for details.

* After building the docker image, make sure that you have set correct information about docker daemon host (IP or domain name) at section `email` in `nthuoj/config/nthuoj.cfg`
