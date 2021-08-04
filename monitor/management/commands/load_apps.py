from django.core.management.base import BaseCommand
from core.cloudfoundry import cf_get_client
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils import timezone

import requests
#import datetime


from monitor.models import Spaces, Orgs, Applications

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


def get_ip_filter_guid(cf_token, space_guid):
    filter_guid = "-1"

    print(f"{bcolours.OKCYAN}Getting guid for ip-filter{bcolours.ENDC}")
    response = requests.get(
        settings.CF_DOMAIN + "/v3/service_instances",
        params={"space_guids": [space_guid, ]},
        headers={"Authorization": f"Bearer {cf_token}"},
    )
    service_response = response.json()
    for service in service_response["resources"]:

        if service["name"] == "ip-filter-service":
            filter_guid = service["guid"]

    return filter_guid


class Command(BaseCommand):


    def handle(self, *args, **options):
        #settings.TIME_ZONE
        print('Running')
        cf_client = cf_get_client(
            settings.CF_USERNAME,
            settings.CF_PASSWORD,
            settings.CF_DOMAIN)

        cf_token = cf_client._access_token

        orgs_list = {'dit-services': '5422b39f-e51b-4dca-a28e-d9bbebf6fefa'}

        # for org in cf_client.v3.organizations.list():
        #     print(f"{bcolours.OKBLUE}{org['name']}{bcolours.ENDC}")
        #     orgs_list[org['name']] = org['guid']

        for org, org_guid in orgs_list.items():
            Orgs.objects.update_or_create(org_name=org, org_guid=org_guid)

            for space in cf_client.v3.spaces.list(organization_guids=org_guid):
                print(f"{bcolours.OKGREEN}{space['name']}{bcolours.ENDC}")
                #filter_guid = get_ip_filter_guid(cf_token, space['guid'])
                # breakpoint()
                Spaces.objects.update_or_create(
                    space_guid=space['guid'], defaults={
                        'space_name': space['name'],
                        #'filter_guid': filter_guid,
                        'orgs': Orgs.objects.get(org_guid=org_guid)
                        }
                    )
                #breakpoint()
                response = requests.get(
                    settings.CF_DOMAIN + "/v3/apps",
                    params={"space_guids": [space['guid'], ]},
                    headers={"Authorization": f"Bearer {cf_token}"},
                )
                app_response = response.json()
                for app in app_response["resources"]:
                    print(app['name'])
                    #breakpoint()
                    Applications.objects.update_or_create(
                        app_guid=app['guid'], defaults={
                            'spaces': Spaces.objects.get(space_guid=space['guid']),
                            'app_name': app['name'],
                            'budget': 100,
                            'budget_left': 100,
                            'budget_reset_date': timezone.now() + relativedelta(weeks=1)
                            }
                        )
