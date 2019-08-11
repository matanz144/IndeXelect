import logging
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
import pandas as pd
from pprint import pprint
from rest_framework.views import APIView
from indexelect_app.index_select import get_indexes
from django.conf import settings

logger = logging.getLogger(__name__)


def get_angular_context():
    context_dict = {}
    for file in os.listdir(settings.ANGULAR_RESOURCES_DIR):
        if file.startswith('runtime') and file.endswith('.js'):
            context_dict['runtime'] = '/static/indexelect-frontend/%s' % file
        if file.startswith('polyfills') and file.endswith('.js'):
            context_dict['polyfills'] = '/static/indexelect-frontend/%s' % file
        if file.startswith('main') and file.endswith('.js'):
            context_dict['main'] = '/static/indexelect-frontend/%s' % file
        if file.startswith('styles') and file.endswith('.css'):
            context_dict['styles'] = '/static/indexelect-frontend/%s' % file
    print(context_dict)
    return context_dict


def home(request):
    return render(request, 'home.html', get_angular_context())


# TODO delete?
def index(request):
    return HttpResponse("Hello, world. You're at the indexelect index.")


# TODO rename?
class RegisterIndexPlateView(APIView):
    def post(self, request):
        parameters = dict()
        data = request.data
        # TODO no need for a for loop here, better to write explicitly: parameters['dist_from_middle'] = ...
        parameters['dist_from_middle'] = float(request.data['dist_from_middle'])
        parameters['num_indexes'] = [int(el) for el in request.data.getlist('num_indexes')]
        parameters['file'] = request.data['file']
        r = ['dist_from_middle', 'num_indexes', 'file']
        for item in r:
            del data[item]
        for key in data:
            parameters[key] = float(request.data[key])
        result = get_indexes(parameters)
        return JsonResponse(data=result, status=200)


# TODO finalize the Excel export file format with Genomics
# Exporting the result to excel file
class ExportToExcelView(APIView):


    def post(self, request): # TODO: add column Index Tag
        print('in ExportToExcelView')

    def post(self, request):

        # TODO rename minVol to min_volume
        minVol = request.data['data']['min_volume']
        vol = {'min volume': [minVol]}
        # TODO remove writer
        writer = pd.ExcelWriter('ExportFile.xlsx', engine='xlsxwriter')

        # create two DataFrames and combine them
        indexes = pd.DataFrame(data=request.data['data']['indexes'])
        volume = pd.DataFrame(vol, columns=['min volume'])
        export = pd.concat([volume, indexes], axis=1, ignore_index=False)
        export = pd.DataFrame.to_json(export)

        return JsonResponse(data={'data': export}, status=200)
