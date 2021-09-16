from prometheus_client import CollectorRegistry, Gauge
import os
import requests
import time
from monitor.models import Applications, Spaces
from django.conf import settings

class PrometheusForecast:

    def __init__(self):
        self.registry = CollectorRegistry()
        self.slaStatsMetric = Gauge('sla_requests_percentage', 'Percentage of requests in a minute', [
                                        'space', 'app', 'le'],registry=self.registry)
        self.slaStatsMetricBreach = Gauge('sla_requests_breach', 'Count of breaches within rolling window', [
                                        'space', 'app', 'le'],registry=self.registry)

    def getRegistry(self):
        return self.registry

    def slaStats(self):
        #breakpoint()
        current_time = round(time.time())
        le_list = ['0.1', '0.25', '0.5', '1', '2.5', '5']
        #le_list = ['1']
        for le in le_list:
            for space in Spaces.objects.values_list("space_name").filter(check_enabled=True):
                no_of_breaches = get_budget_count(space[0], le, current_time)
                #print(no_of_breaches)
                for key, value in no_of_breaches.items():
                    #print(key, value)
                    self.slaStatsMetricBreach.labels(space[0],key,le).set(value)

                results = run_prom(space[0], le, current_time)

                for response in results:
                    self.slaStatsMetric.labels(space[0],response['metric']['app'],le).set(response['value'][1])



def run_prom(space, le, current_time):
    url = f'{settings.PROM_URL}/api/v1/query'
    #breakpoint()
    params = {
    'query': f'((sum by (app)(increase(response_time_bucket{{space="{space}", status_range="2xx", le="{le}"}}[1m] @{current_time})) / sum by (app)(increase(response_time_bucket{{status_range="2xx", le="+Inf"}}[1m] @{current_time})))*100)>0'
    }
    response = requests.get(url, params=params).json()['data']['result']

    return response


def get_budget_count(space, le, current_time):
    #url = 'http://localhost:9090/api/v1/query'
    url = f'{settings.PROM_URL}/api/v1/query'

    params = {
    'query': f'(sla_budget{{space="{space}"}} [{settings.ROLLING_SLA_WINDOW_SIZE}h] @{current_time})'
    }
    response = requests.get(url, params=params).json()['data']['result']

    count_list = {}
    for app in response:
        count_items = 0
        for value in (app['values']):
            if float(value[1]) < float(settings.SLA_THRESHOLD):
                count_items +=1

        count_list[app['metric']['app']] = count_items

    return count_list
