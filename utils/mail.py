import os.path
from docker import Client
from docker.tls import TLSConfig
from requests.exceptions import ConnectionError, ReadTimeout
from django.conf import settings

from utils.config_info import get_config
from utils.log_info import get_logger

HOST = get_config('email', 'host')
PORT = 2376
BASE_URL = "tcp://%s:%s" % (HOST, PORT)
IMAGE = "oj_mail"
DOCKER_TLS_CERT_PATH = get_config('email', 'docker_tls_cert_path')
CERT = os.path.realpath(os.path.join(DOCKER_TLS_CERT_PATH, 'cert.pem'))
KEY = os.path.realpath(os.path.join(DOCKER_TLS_CERT_PATH, 'key.pem'))

logger = get_logger()


class MailSender():

    def __init__(self, body, subject, username, email):
        self.CMD = ["sh", "send_mail.sh", body, subject, email]
        self.TO = "%s(%s)" % (username, email)

    def _send(self):
        tls_config = TLSConfig(client_cert=(CERT, KEY))
        cli = Client(base_url=BASE_URL, tls=tls_config)
        container = cli.create_container(image=IMAGE, command=self.CMD)
        container_id = container.get("Id")
        cli.start(container=container_id)
        try:
            cli.wait(container=container_id, timeout=10)
        finally:
            cli.remove_container(container=container_id, force=True)

    def send(self):
        try:
            self._send()
            logger.info("Send email to %s successfully." % self.TO)
        except ConnectionError:
            logger.warning("Failed to send email to %s! Cannot connect to docker daemon!" % self.TO)
        except ReadTimeout:
            logger.warning("Might fail to send email to %s! Request timeout!" % self.TO)
        except:
            logger.warning("Something went wrong when sending email to %s." % self.TO)
