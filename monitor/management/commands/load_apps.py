from django.core.management.base import BaseCommand
from core.cloudfoundry import cf_get_client
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils import timezone

import requests

from monitor.models import Spaces, Orgs

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


class Command(BaseCommand):


    def handle(self, *args, **options):
        print('Running')
        cf_client = cf_get_client(
            settings.CF_USERNAME,
            settings.CF_PASSWORD,
            settings.CF_DOMAIN)

        cf_token = cf_client._access_token

        orgs_list = settings.ORG_GUID

        # for org in cf_client.v3.organizations.list():
        #     print(f"{bcolours.OKBLUE}{org['name']}{bcolours.ENDC}")
        #     orgs_list[org['name']] = org['guid']

        for org, org_guid in orgs_list.items():
            Orgs.objects.update_or_create(org_name=org, org_guid=org_guid)

            for space in cf_client.v3.spaces.list(organization_guids=org_guid):
                print(f"{bcolours.OKGREEN}{space['name']}{bcolours.ENDC}")

                Spaces.objects.update_or_create(
                    space_guid=space['guid'], defaults={
                        'space_name': space['name'],
                        'orgs': Orgs.objects.get(org_guid=org_guid)
                        }
                    )
                #breakpoint()
