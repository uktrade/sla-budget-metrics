
import geckoboard as gb

from django.conf import settings

from django.core.management.base import BaseCommand
from django.conf import settings

from time import sleep
import traceback

from monitor.models import Applications, Spaces


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.send_gecko_report()

    def send_gecko_report(self):
        self.count = 0
        GECKO_API_TOKEN = settings.GECKO_TOKEN

        try:
            gbClient = gb.client(GECKO_API_TOKEN)
            gbClient.ping()
            self.__push_overview__(gbClient=gbClient)
        except Exception as e:
            print("GeckoReport Error:{}".format(e))
            traceback.print_exc()

    ### overview report ###
    def __push_overview__(self, gbClient):
        #self.__wait__()
        #breakpoint()

        report = []#{'app_name': [], 'space': [], 'budget_remaining': []}
        #breakpoint()
        for app_obj in Applications.objects.filter(spaces__space_name='directory'):

            data = {
                'app_name': app_obj.app_name,
                'space': 'directory',
                'budget_remaining': app_obj.budget_left
                }
            report.append(data)

        #print(report)
        dataset = gbClient.datasets.find_or_create('paas.sla.budget.space',
                                                   {
                                                       'app_name': {'type': 'string', 'name': 'app_name'},
                                                       'space': {'type': 'string', 'name': 'space'},
                                                       'budget_remaining': {'type': 'number', 'name': 'budget_remaining'}
                                                   },
                                                   )
        dataset.put([])
        dataset.put(report)
        # dataset.put([
        #     {
        #         'app_name': 'great-international-ui',
        #         'space': 'directory',
        #         'budget_remaining': 80
        #     },
        #     {
        #         'app_name': 'great-domestic-ui',
        #         'space': 'directory',
        #         'budget_remaining': 60
        #     }
        #     ]
        # )
        #
        # self.count += 3


    # wait if count if more than 50
    # This is to ensure we are not sending more than 60 push request a minute as per the limit set by Geckoboard
    def __wait__(self):
        if self.count >= 50:
            sleep(65)
            self.count = 0
