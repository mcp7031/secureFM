from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from api.utils.exceptionhandler import custom_exception_handler
from rest_framework.views import APIView

# Create your views here.
# class query_tenant(APIView):
    
@api_view()
def query_tenant(request):
    x = 1
    y = 2
#  return HttpResponse('return from query_tenant function')
#  return render(request, 'tenant.html', {'name' : 'David'})
    return Response('return from query_tenant function in the ppt module')
