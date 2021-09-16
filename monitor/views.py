import requests

from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from monitor.helper.prometheus import PrometheusForecast
from django.contrib.auth.decorators import login_required
import prometheus_client


class home_page(View):
    template_name = 'home-page.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)


class metrics_page(View):

    #@method_decorator(login_required)
    def get(self, request):
        pf = PrometheusForecast()
        registry = pf.getRegistry()

        pf.slaStats()

        metric = prometheus_client.exposition.generate_latest(registry)
        return HttpResponse(metric,content_type=prometheus_client.exposition.CONTENT_TYPE_LATEST)
