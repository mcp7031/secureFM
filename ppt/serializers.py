from rest_framework import serializers
from .models import Nominal, Tenant, Documents,\
        Services, BIMMbyLocation, Location,\
        BIMM, BIM, BIMMbyBIM, CostCentre, Personnel, \
        Contractor, Company
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

class PersonnelDocumentSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source='nominal_ptr_id')
    name = serializers.SerializerMethodField(method_name='get_name')
    company = serializers.SerializerMethodField(method_name='get_company')
    documents = serializers.SerializerMethodField(method_name='get_documents')
    service = serializers.SerializerMethodField(method_name='get_service')
    contactL1 = serializers.SerializerMethodField(method_name='get_contactL1')
    contactL2 = serializers.SerializerMethodField(method_name='get_contactL2')
    contactL3 = serializers.SerializerMethodField(method_name='get_contactL3')
    

    def get_name(self, nominal: Nominal):
        return nominal.lastName+", "+nominal.firstName

    def get_contactL1(self, person: Personnel):
        id = person.contractor_id
        co = Contractor.objects.get(contractor_id=id)
        contactL1 = Nominal.objects.select_related().filter(nominal_id=co.contactL1_id)
        return contactL1.values('lastName', 'firstName', 'mobile')
    def get_contactL2(self, person: Personnel):
        id = person.contractor_id
        co = Contractor.objects.get(contractor_id=id)
        contactL2 = Nominal.objects.select_related().filter(nominal_id=co.contactL2_id)
        return contactL2.values('lastName', 'firstName', 'mobile')
    def get_contactL3(self, person: Personnel):
        id = person.contractor_id
        co = Contractor.objects.get(contractor_id=id)
        contactL3 = Nominal.objects.select_related().filter(nominal_id=co.contactL3_id)
        return contactL3.values('lastName', 'firstName', 'mobile')

    def get_documents(self, nominal: Nominal):
        documentSet = Documents.objects.select_related().filter(nominal_id=nominal.nominal_id)
        return documentSet.values('docName', 'docDesc')

    def get_service(self, nominal: Nominal):
        service = Services.objects.select_related().filter(services_id=nominal.services_id)
        return service.values('serviceName')
   
    def get_company(self, personnel: Personnel):
        co = Contractor.objects.select_related().filter(contractor_id=personnel.contractor_id)
        return co.values('companyName', 'companyNumber', 'companyPhone')

    class Meta:
        model = Personnel
        fields = ('number', 'name', 'dateStart', 'company', 'service', 'contactL1', 'contactL2', 'contactL3', 'documents')

class CompanySerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source='company_id')
    contactL1 = serializers.SerializerMethodField(method_name='get_contactL1')
    contactL2 = serializers.SerializerMethodField(method_name='get_contactL2')
    contactL3 = serializers.SerializerMethodField(method_name='get_contactL3')
    
    def get_contactL1(self, co: Company):
        contactL1 = Nominal.objects.select_related().filter(nominal_id=co.contactL1_id)
        return contactL1.values('lastName', 'firstName', 'mobile')
    def get_contactL2(self, co: Company):
        contactL2 = Nominal.objects.select_related().filter(nominal_id=co.contactL2_id)
        return contactL2.values('lastName', 'firstName', 'mobile')
    def get_contactL3(self, co: Company):
        contactL3 = Nominal.objects.select_related().filter(nominal_id=co.contactL3_id)
        return contactL3.values('lastName', 'firstName', 'mobile')
    
    class Meta:
        model = Company
        fields = ('number', 'compName', 'tradeName', 'contactL1', 'contactL2', 'contactL3')

class CostCentreSerializer(serializers.ModelSerializer):
    contactL1 = serializers.SerializerMethodField(method_name='get_contactL1')
    contactL2 = serializers.SerializerMethodField(method_name='get_contactL2')
    contactL3 = serializers.SerializerMethodField(method_name='get_contactL3')
    number = serializers.IntegerField(source='costCentre_id')
    
    def get_contactL1(self, cc: CostCentre):
        contactL1 = Nominal.objects.select_related().filter(nominal_id=cc.contactL1_id)
        return contactL1.values('lastName', 'firstName', 'mobile')
    def get_contactL2(self, cc: CostCentre):
        contactL2 = Nominal.objects.select_related().filter(nominal_id=cc.contactL2_id)
        return contactL2.values('lastName', 'firstName', 'mobile')
    def get_contactL3(self, cc: CostCentre):
        contactL3 = Nominal.objects.select_related().filter(nominal_id=cc.contactL3_id)
        return contactL3.values('lastName', 'firstName', 'mobile')
    
    class Meta:
        model = CostCentre
        fields = ('number', 'costName', 'costAccount', 'contactL1', 'contactL2', 'contactL3')


class LocationSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source='location_id')
#    costCentre = serializers.SerializerMethodField(method_name='get_cc')
    costCentre = CostCentreSerializer(many=False, read_only=True)

    def get_cc(self, location: Location):
#        cc = CostCentre.objects.get(costCentre_id=location.costCentre_id)
        contactL1 = serializers.SerializerMethodField(method_name='get_contact')
        ccSet = CostCentre.objects.select_related().filter(costCentre_id=location.costCentre_id)
        return ccSet.values('costName', 'costAccount', 'contactL1_id')

    def get_contact(self, cc: costCentre):
        nomSet = Nominal.objects.select_related().filter(nominal_id=cc.contactL1_id)
        return nomSet.values('lastName'+', '+'firstName')

    class Meta:
        model = Location
        fields = ('number', 'locationCode', 'description', 'length', 'width', 'costCentre')

class LocationBIMMSerializer(serializers.ModelSerializer):
    Number = serializers.IntegerField(source='location_id')
    BIMMitems = serializers.SerializerMethodField(method_name='get_bimm')

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
        fields = ('Number', 'locationCode', 'description', 'BIMMitems')

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

