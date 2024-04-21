from django.shortcuts import get_object_or_404 
from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
#from api.utils.exceptionhandler import custom_exception_handler
from rest_framework.views import APIView
from .models import Tenant, Location, BIMM, CostCentre, Contractor, Personnel, Company
from . import serializers
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class QueryAllCompany(APIView):

    def get(self, request):
        queryset = Company.objects.all()
        serializer = serializers.CompanySerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request, pid, format=None):
        queryset = self.get_object(pid)
        serializer = serializers.CompanySerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class QueryCompany(APIView):

    def get_object(self, pk):
        try:
            return Company.objects.get(company_id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def check_object(self, pk):
        try:
            return Company.objects.get(company_id=pk)
        except ObjectDoesNotExist:
            return 

    def get(self, request, pid):
#        queryset = self.get_object(pid)
        queryset = get_object_or_404(Company, pk=pid)
        serializer = serializers.CompanySerializer(
           queryset, many=False, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pid):
        queryset = get_object_or_404(Company, pk=pid)
        serializer = serializers.CompanySerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pid):
        queryset = get_object_or_404(Company, pk=pid)
        num = request.GET['number']
        cn = request.GET['compName']
        tn = request.GET['tradeName']
        pdata = { 
                'number': num,
                'compName': cn,
                'tradeName': tn,
                }
        serializer = serializers.CompanySerializer(
           queryset, data=pdata)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pid, format=None):
        queryset = self.check_object(pid)
        if (queryset):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        num = request.GET['number']
        cn = request.GET['compName']
        tn = request.GET['tradeName']
        pdata = { 
                'number': num,
                'compName': cn,
                'tradeName': tn,
                }
        serializer = serializers.CompanySerializer(
           queryset, data=pdata)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pid):
        queryset = get_object_or_404(Company, pk=pid)
        if (not queryset):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        num = request.GET['number']
        cn = request.GET['compName']
        tn = request.GET['tradeName']
        pdata = { 
                'number': num,
                'compName': cn,
                'tradeName': tn,
                }
        serializer = serializers.CompanySerializer(
           queryset, data=pdata)
        if (serializer.is_valid()):
           count = Company.objects.filter(compName=cn).delete()
           return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QueryAllCostCentres(APIView):

    def get(self, request):
        queryset = CostCentre.objects.all()
        serializer = serializers.CostCentreSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request, pid, format=None):
        queryset = self.get_object(pid)
        serializer = serializers.CostCentreSerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class QueryCostCentres(APIView):

    def get_object(self, pk):
        try:
            return CostCentre.objects.get(costCentre_id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def check_object(self, pk):
        try:
            return CostCentre.objects.get(costCentre_id=pk)
        except ObjectDoesNotExist:
            return 

    def get(self, request, pid):
        queryset = self.get_object(pid)
        serializer = serializers.CostCentreSerializer(
           queryset, many=False, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request, pid, format=None):
        queryset = self.check_object(pid)
        if (queryset):
            return Response(status=status.HTTP_226_IM_USED)
        serializer = serializers.CostCentreSerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class QueryAllTenantDocuments(APIView):

    def get(self, request):
        queryset = Tenant.objects.all()
        serializer = serializers.TenantDocumentSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
                 
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

    def post(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class QueryAllPersonnel(APIView):

    def get(self, request):
        queryset = Personnel.objects.all()
        serializer = serializers.PersonnelDocumentSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
                 
class QueryPersonnel(APIView):

    def get_object(self, pk):
        try:
            return Personnel.objects.get(nominal_ptr_id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pid, format=None):
        print("this is the request: "+str(request))
        queryset = self.get_object(pid)
        serializer = serializers.PersonnelDocumentSerializer(
           queryset, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pid, format=None):
        queryset = self.get_object(pid)
        serializer = serializers.PersonnelDocumentSerializer(
           queryset, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class QueryAllLocationsBIMM(APIView):

    def get(self, request):
        queryset = Location.objects.all()
        serializer = serializers.LocationBIMMSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class QueryLocationBIMM(APIView):

    def get_object(self, pk):
        try:
            return Location.objects.get(location_id=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pid, format=None):
        print("this is the request: "+str(request))
        queryset = self.get_object(pid)
        serializer = serializers.LocationBIMMSerializer(
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

    def post(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, pid, format=None):
        print("in QueryLocationBIMM request data->"+str(request.data)+"<-")
        queryset = self.get_object(pid)
        print("queryset ->"+str(queryset)+"<-")
        serializer = serializers.LocationSerializer(
           queryset, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class QueryAllBIMM(APIView):

    def get(self, request):
        queryset = BIMM.objects.all()
        serializer = serializers.BIMMSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class QueryAllLocations(APIView):

    def get(self, request):
        queryset = Location.objects.all()
        serializer = serializers.LocationSerializer(
           queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class QueryLocation(APIView):

    def get_object(self, pk):
        try:
            return Location.objects.get(location_id=pk)
        except ObjectDoesNotExist:
            raise Http404("Location does not exist")

    def get(self, request, pid, format=None):
        print("in QueryLocation this is the request: "+str(request))
        queryset = self.get_object(pid)
        serializer = serializers.LocationSerializer(
           queryset, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pid, format=None):
        queryset = self.get_object(pid)  # for POST the object should not exist generate 404
        serializer = serializers.LocationSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pid, format=None):
#        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        queryset = self.get_object(pid)  # for POST the object should already exist
        print("POST queryset ->"+str(queryset)+"<-")
        serializer = serializers.LocationSerializer(data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pid, format=None):
        print("in QueryLocation request data->"+str(request)+"<- pid ->"+str(pid)+"<-")
        queryset = self.get_object(pid)
        
        print("queryset ->"+str(queryset)+"<-")
        serializer = serializers.LocationSerializer(
           queryset, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pid, format=None):
        queryset = self.get_object(pid)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
