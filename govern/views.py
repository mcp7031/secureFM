from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def query_govern(request):
    x = 1
    y = 2
    return HttpResponse('return from query_govern function')
