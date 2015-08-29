from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse,Http404
import datetime,time
from urllib import unquote

def hello(request):
    return HttpResponse("URL: http://%s%s" % (request.get_host(), request.get_full_path()))
