from rest_framework import serializers
from .models import Nominal, Tenant, Documents, Services, BIMMbyLocation, Location, BIMM, BIM, BIMMbyBIM
from pymongo import MongoClient
from djongo import models as mongo
# from itertools import chain

class TenantDocumentSerializer(serializers.ModelSerializer):
    tenantNumber = serializers.IntegerField(source='nominal_ptr_id')
    tenantName = serializers.SerializerMethodField(method_name='tenant_name')
    tenantDocuments = serializers.SerializerMethodField(method_name='get_documents')
    tenantService = serializers.SerializerMethodField(method_name='get_service')

    def tenant_name(self, nominal: Nominal):
        return nominal.lastName+", "+nominal.firstName

    def get_documents(self, nominal: Nominal):
        documentSet = Documents.objects.select_related().filter(nominal_id=nominal.nominal_id)
        return documentSet.values('docName', 'docDesc')

    def get_service(self, nominal: Nominal):
        service = Services.objects.select_related().filter(services_id=nominal.services_id)
        return service.values('serviceName')

    class Meta:
        model = Tenant
        fields = ('tenantNumber', 'tenantName', 'companyName', 'tenantService', 'tenantDocuments')

class DocumentSerializer(serializers.ModelSerializer):
    documentSet = serializers.SerializerMethodField(method_name='document_set')

    def document_set(self, nominal: Nominal):
        return Documents.objects.select_related().filter(nominal_id=nominal.nominal_id)

    class Meta:
        model = Documents
        fields = ('docName', 'docDesc')
        
class LocationSerializer(serializers.ModelSerializer):
    locNumber = serializers.IntegerField(source='location_id')
    bimmbyloc = serializers.SerializerMethodField(method_name='get_bimm')
#        BIMMobjects = mongo.DjongoManager()

    def get_bimm(self, location: Location):
        bimmLocSet = BIMMbyLocation.objects.select_related().filter(location_id=location.location_id)
        bimmSet = BIMM.objects.distinct().filter(bimm_id__in=bimmLocSet)
        docList = bimmSet.values_list('bimm_id')
        print("BIMM Set "+str(docList))
        for id in docList:
            print("bimm id: "+str(id))
     #   return bimmLocSet.values('bimm_id', 'dateModified', 'note') 
      
        return  bimmSet.values('bimm_id', 'name', 'description', 'safety', 'manual', 'iotURL', 'iotDevice') 

    class Meta:
        model = Location
        fields = ('locNumber', 'locationCode', 'description', 'bimmbyloc')

class BIMMSerializer(serializers.ModelSerializer):
    bimmNumber = serializers.IntegerField(source='bimm_id')
    locations = serializers.SerializerMethodField(method_name='get_loc')
    BIMelements = serializers.SerializerMethodField(method_name='get_bim')
    BIMnote = serializers.SerializerMethodField(method_name='get_note')

    def get_xref(self, bimm: BIMM):
        return BIMMbyBIM.objects.select_related().filter(bimm_id=bimm.bimm_id)

    def get_note(self, bimm: BIMM):
        bimmBimSet = self.get_xref(bimm)
        return bimmBimSet.values('bim_id', 'dateModified', 'note')

    def get_bim(self, bimm: BIMM):
        bimmBimSet = self.get_xref(bimm)
#        bimmBimSet.modified = serializers.DateTimeField(source='bimmBimSet.dateModified')
#        bimmBimSet.note = serializers.CharField(max_length=255, source='bimmBimSet.note')
        bimSet = BIM.objects.distinct().filter(bim_id__in=bimmBimSet)
        return bimSet.values('bim_id', 'name', 'description', 'mongoDB_id')

    def get_loc(self, bimm: BIMM):
        bimmLocSet = BIMMbyLocation.objects.select_related().filter(bimm_id=bimm.bimm_id)
        bimmSet = Location.objects.distinct().filter(location_id__in=bimmLocSet)
#        locList = bimmSet.values_list('location_id')
      
        return  bimmSet.values('location_id', 'locationCode', 'description') 

    class Meta:
        model = BIMM
        fields = ('bimmNumber', 'name', 'description', 'purchaseDate', 'locations', 'warranty', 'mtbf', 'hoursToDate', 'BIMelements', 'BIMnote')

