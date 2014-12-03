import getpass

# Setting nthuoj.ini
host = raw_input("Mysql host: ")
db = raw_input("Mysql database: ")
user = raw_input("Please input your mysql user: ")
pwd = getpass.getpass()

# Re-write nthuoj.ini file
iniFile = open("nthuoj.ini", "w")
iniFile.write("[client]\n")
iniFile.write("host = %s\n" % host)
iniFile.write("database = %s\n" % db)
iniFile.write("user = %s\n" % user)
iniFile.write("password = %s\n" % pwd)
iniFile.write("default-character-set = utf8\n")
iniFile.close()


# Install needed library

