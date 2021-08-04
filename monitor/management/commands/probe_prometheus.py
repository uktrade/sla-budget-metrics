from django.core.management.base import BaseCommand

import requests
import json
import traceback

from monitor.models import Applications, Spaces


def update_budget(app_name, threshold_breach, space):
    #breakpoint()
    print(space + ' ' + app_name)
    #try:
    app_obj = Applications.objects.get(app_name=app_name, spaces__space_name=space)
    #except Applications.MultipleObjectsReturned:

        #breakpoint()
        #app_obj = Applications.objects.filter(app_name=app_name, spaces__space_name=space)[0]

    #breakpoint()
    new_budget = app_obj.budget_left - int(float(threshold_breach))

    # Applications.objects.update_or_create(
    #         app_name=app_name, defaults={"budget_left": new_budget}
    #     )
    app_obj.budget_left=new_budget
    app_obj.save


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://dit-prometheus.london.cloudapps.digital/api/v1/query'

        # params = {
        # 'query':'sum by (app)(increase(response_time_bucket{app="great-international-ui", status_range="2xx", le="+Inf"}[1m])) - sum by (app)(increase(response_time_bucket{ status_range="2xx", le="1"}[1m]))'
        # }
        #breakpoint()
        for space in Spaces.objects.values_list("space_name").filter(check_enabled=True):

            # params = {
            # 'query': f'sum by (app)(increase(response_time_bucket{{space="{space[0]}", status_range="2xx", le="+Inf"}}[1m])) - sum by (app)(increase(response_time_bucket{{ status_range="2xx", le="1"}}[1m]))'
            # }
            # % per hour
            params = {
            'query': f'((sum by (app)(increase(response_time_bucket{{space="{space[0]}", status_range="2xx", le="+Inf"}}[1h])) - sum by (app)(increase(response_time_bucket{{ status_range="2xx", le="1"}}[1h])))/(sum by (app)(increase(response_time_bucket{{ status_range="2xx", le="+Inf"}}[1h])))*100)>0'
            }


            response = requests.get(url, params=params).json()

            #breakpoint()
            for app in response['data']['result']:

                update_budget(app['metric']['app'], app['value'][1], space[0])
