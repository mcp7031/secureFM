from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.exceptions import APIException

# Create your views here.
@api_view()
def query_imanage(request):
    x = 1
    y = 2
#  return HttpResponse('return from query_imanage function')
#   return render(request, 'imanage.html')
    return Response('return from query_imanage function')

@api_view()
def query_current(request):
    return Response('return from query_current function in the Incident Management Module')
