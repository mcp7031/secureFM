from django.shortcuts import render
from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from api.utils.exceptionhandler import custom_exception_handler
from rest_framework.views import APIView
from .models import Tenant, Location, BIMM
from . import serializers
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class QueryAllTenantDocuments(APIView):

    def get(self, request):
        queryset = Tenant.objects.all()
        serializer = serializers.TenantDocumentSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        pass
        return
                 
class QueryTenantDocuments(APIView):

    def get_object(self, pk):
        try:
            return Tenant.objects.get(nominal_ptr_id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pid, format=None):
        print("this is the request: "+str(request))
        queryset = self.get_object(pid)
        serializer = serializers.TenantDocumentSerializer(
           queryset, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pid, format=None):
        queryset = self.get_object(pid)
        serializer = serializers.TenantDocumentSerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryAllLocations(APIView):

    def get(self, request):
        queryset = Location.objects.all()
        serializer = serializers.LocationSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        pass
        return

class QueryLocation(APIView):

    def get_object(self, pk):
        try:
            return Location.objects.get(location_id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pid, format=None):
        print("this is the request: "+str(request))
        queryset = self.get_object(pid)
        serializer = serializers.LocationSerializer(
           queryset, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pid, format=None):
        queryset = self.get_object(pid)
        serializer = serializers.LocationSerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QueryAllBIMM(APIView):

    def get(self, request):
        queryset = BIMM.objects.all()
        serializer = serializers.BIMMSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        pass
        return
    
class QueryBIMM(APIView):

    def get_object(self, pid):
        try:
            return BIMM.objects.get(bimm_id=pid)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pid, format=None):
        print("this is the request: "+str(request))
        queryset = self.get_object(pid)
        serializer = serializers.BIMMSerializer(
           queryset, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pid, format=None):
        queryset = self.get_object(pid)
        serializer = serializers.BIMMSerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view()
def query_tenant(request):
    x = 1
    y = 2
#  return HttpResponse('return from query_tenant function')
#  return render(request, 'tenant.html', {'name' : 'David'})
    return Response('return from query_tenant function in the ppt module')
