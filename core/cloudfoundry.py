import requests
import json

from cloudfoundry_client.client import CloudFoundryClient
from django.conf import settings

#from monitor.models import Spaces, Applications


class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cf_get_client(username, password, endpoint, http_proxy="", https_proxy=""):
    target_endpoint = endpoint
    proxy = dict(http=http_proxy, https=https_proxy)
    client = CloudFoundryClient(target_endpoint, proxy=proxy)
    client.init_with_user_credentials(username, password)
    return client


def cf_login():
    cf_client = cf_get_client(settings.CF_USERNAME, settings.CF_PASSWORD, settings.CF_DOMAIN)
    return cf_client
