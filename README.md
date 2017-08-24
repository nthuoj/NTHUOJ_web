# NTHUOJ_web
Version 1.0.4
[![Build Status](https://travis-ci.org/henryyang42/NTHUOJ_web.svg)](https://travis-ci.org/henryyang42/NTHUOJ_web)


## Getting Started

### Get our project
```
git clone https://github.com/nthuoj/NTHUOJ_web.git
```

### Config Git for installing Bower dependencies
```
git config --global url."https://".insteadOf git://
```

### Installation
* Install dependencies (for Ubuntu)
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

* Run install.py setup settings.
```
python install.py
```
* Please DO **NOT** run this command with sudo to prevent further errors in permission setttings.
* Settings without concerning to the database connection can be left blank and modified in `NTHUOJ_web/nthuoj/config/nthuoj.cfg` later.
* Our project will not automatically generate a database. Therefore, you would like to create a local database on your own.

### Email host
* The email host should be Gmail.
* The Google account setting ```Access for less secure apps``` should be turned on.

### Email:
* In our project, we use **Postfix** as the mail server for sending emails of registration or resetting password.

* It's recommended that you install our project on a machine which has an IP address or a domain name belongs to NTHU, or outgoing emails would almost definitely be blocked by other mail service providers.

* The mail server will be installed in a docker image, so if you want to enable email sending, you have to build the image first. Please check [here](https://github.com/nthuoj/NTHUOJ_web_docker) for details.

* After building the docker image, make sure that you have set correct information about docker daemon host (IP or domain name) at section `email` in `nthuoj/config/nthuoj.cfg`

## Reference
* For more detailed deployment instructions, please follow the [NTHUOJ_deploy](https://gist.github.com/henryyang42/e70c7f444788e674c4da) note.
* To install in a docker container, please refer to the [NTHUOJ_web_docker](https://github.com/nthuoj/NTHUOJ_web_docker) repository.

## License
NTHUOJ_web is licensed under the terms of the [MIT license](https://github.com/nthuoj/NTHUOJ_web/blob/master/LICENSE).

