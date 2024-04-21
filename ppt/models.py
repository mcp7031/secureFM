from pyexpat import model
from djongo import models as mongo
from operator import mod
from django.contrib.auth import get_user_model
from django.db import models
from ppt.utils import _get_addRole
# from django.contrib.mysql.fields import JSONField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Blob(mongo.Model):
    name = mongo.CharField(max_length=100)
    tagline = mongo.TextField()
    
    class Meta:
        abstract = True

class Nominal(models.Model):
    nominal_id = models.AutoField(primary_key=True)
    location = models.ForeignKey('Location', blank=True, null=True, on_delete=models.PROTECT)
    costCentre = models.ForeignKey('CostCentre', blank=True, null=True, on_delete=models.PROTECT)
    dateCreated = models.DateTimeField(editable=False, default=timezone.now)
    createdBy = models.ForeignKey('self', null=True, blank=True, related_name='+', verbose_name='Created By', on_delete=models.PROTECT)
    dateBirth = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='Date of birth')
    lastName = models.CharField(max_length=255, verbose_name='Last Name')
    firstName = models.CharField(max_length=255, verbose_name='First Name')
    middleName = models.CharField(max_length=255, null=True, blank=True, verbose_name='Middle Name')
    driverLicense = models.IntegerField(blank=True, null=True, verbose_name='Driver License')
    driverClass = models.CharField(max_length=4, default='C', verbose_name='Class of License') 
#    address1 = AddressField(blank=True, null=True, verbose_name='Address Line 1')
#    address2 = AddressField(related_name='+', blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address Line 1')
    address2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address Line 2')
    phone = PhoneNumberField(unique=True, null=True, blank=True, verbose_name='Contact phone number')
    mobile = PhoneNumberField(unique=True, null=True, blank=True, verbose_name='Mobile number')
#    safety = models.CharField(max_length=40, blank=True, null=True, verbose_name='Safety Documentation')
#    incident = models.CharField(max_length=40, blank=True, null=True, verbose_name='Incident Documentation')

    class Meta:
        ordering=['lastName']

    def __str__(self):
        return self.lastName+", "+self.firstName
    
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    tradeName = models.CharField(max_length=255, verbose_name='Company Name')
    compName = models.CharField(max_length=255, verbose_name='Trade Name')
    abn = models.CharField(editable=True, max_length=8, verbose_name='ABN')
    account = models.CharField(default='999-999-9999', editable=True, max_length=12, verbose_name='G/L account number')
    contactL1 = models.ForeignKey(Nominal, null=True, blank=True, related_name='+', verbose_name='Level 1 Contact', on_delete=models.PROTECT)
    contactL2 = models.ForeignKey(Nominal, null=True, blank=True, related_name='+', verbose_name='Level 2 Contact', on_delete=models.PROTECT)
    contactL3 = models.ForeignKey(Nominal, null=True,  blank=True, related_name='+', verbose_name='Level 3 Contact', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.tradeName


class CostCentre(models.Model):
    costCentre_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    costName = models.CharField(max_length=255, verbose_name='Cost Centre')
    costAccount = models.CharField(default='999-999-9999', max_length=12, verbose_name='G/L account number')
    contactL1 = models.ForeignKey(Nominal, null=True, blank=True, verbose_name='Level 1 Contact', related_name='+', on_delete=models.PROTECT)
    contactL2 = models.ForeignKey(Nominal, null=True, blank=True, verbose_name='Level 2 Contact', related_name='+', on_delete=models.PROTECT)
    contactL3 = models.ForeignKey(Nominal, null=True, blank=True, verbose_name='Level 3 Contact', related_name='+', on_delete=models.PROTECT)

    class Meta:
        ordering=['costName']

    def __str__(self) -> str:
        return self.costName 

class AccessGroups(models.Model):
    accessGroup_id = models.AutoField(primary_key=True)
    groupCode = models.CharField(max_length=6)
    groupName = models.CharField(max_length=255)
    accessLevel = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering=['groupCode']

class BIM(models.Model):
    bim_id = models.AutoField(primary_key=True)
    name = models.CharField(default='default', max_length=255)
    description = models.TextField(blank=True, null=True)
    mongoDB_id = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        ordering=['name']

class BIMM(models.Model):
    bimm_id = models.AutoField(primary_key=True)
    name = models.CharField(default='default', max_length=255,verbose_name='Name')
    description = models.TextField(blank=True, null=True,verbose_name='Description')
    purchaseDate = models.DateTimeField(blank=True, null=True, verbose_name='Purchase Date')
    warranty = models.CharField(max_length=40, blank=True, null=True, verbose_name='Warranty Documents')
    note = models.TextField(blank=True, null=True, verbose_name='Notes')
    mtbf = models.IntegerField(blank=True, null=True, verbose_name='MTBF (in hours)')
    hoursToDate = models.IntegerField(blank=True, null=True)
    safety = models.CharField(max_length=40, blank=True, null=True, verbose_name='Safety Documentation')
    manual = models.CharField(max_length=40, blank=True, null=True, verbose_name='Operating Manual')
    msds = models.CharField(max_length=40, blank=True, null=True, verbose_name='MSDS')
    iotURL = models.CharField(max_length=255, blank=True, null=True)
    iotDevice = models.CharField(max_length=255, blank=True, null=True)
    bimmbyBIM = models.ManyToManyField(BIM, through='BIMMbyBIM')
    reviewedDate = models.DateTimeField(blank=True, null=True, verbose_name='Reviewed Date')
    reviewedBy = models.ForeignKey(Nominal, null=True, blank=True, related_name='+', verbose_name='Reviewed By', on_delete=models.PROTECT)

    class Meta:
        ordering=['name']

    def __str__(self):
        return self.name

class serviceLog(models.Model):
    serviceLog_id = models.AutoField(primary_key=True)
    logDate = models.DateTimeField()
    bimm = models.ForeignKey(BIMM, on_delete=models.PROTECT)
    who = models.ForeignKey(Nominal, on_delete=models.PROTECT)
    note = models.TextField()        

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    costCentre = models.ForeignKey(CostCentre, on_delete=models.CASCADE)
    locationCode = models.CharField(max_length=26)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Description')
    length = models.IntegerField(blank=True, null=True, verbose_name='Length')
    width = models.IntegerField(blank=True, null=True, verbose_name='Width')
    bimmbyloc = models.ManyToManyField(BIMM, through='BIMMbyLocation')

    class Meta:
        ordering=['costCentre', 'locationCode']

    def __str__(self):
        return self.locationCode

class BIMMbyLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    bimm = models.ForeignKey(BIMM, on_delete=models.PROTECT)
    dateModified = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)

class BIMMbyBIM(models.Model):
    bim = models.ForeignKey(BIM, on_delete=models.PROTECT)
    bimm = models.ForeignKey(BIMM, on_delete=models.PROTECT)
    dateModified = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)

class LocationGroupAccess(models.Model):
    locationGroupAccess_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, related_name='+', on_delete=models.PROTECT)
    accessGroup = models.ForeignKey(AccessGroups, related_name='+', on_delete=models.PROTECT)

    def __str__(self):
        return self.accessGroup

class NominalGroupAccess(models.Model):
    nominalGroupAccess_id = models.AutoField(primary_key=True)
    nominal = models.ForeignKey(Nominal, related_name='+', on_delete=models.PROTECT)
    accessGroup = models.ForeignKey(AccessGroups, related_name='+', on_delete=models.PROTECT)

    class Meta:
        ordering=['nominal']

    def __str__(self):
        return self.nominal+" "+self.accessGroup

class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    nominal = models.ForeignKey(Nominal, on_delete=models.CASCADE)
    docName = models.CharField(max_length=255, verbose_name='name of document')
    docDesc = models.TextField(blank=True, null=True)
    document = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        ordering=['nominal', 'docName']

    def __str(self):
        return self.nominal+" "+self.docName

class Services(models.Model):
    services_id = models.AutoField(primary_key=True)
    serviceCode = models.CharField(max_length=6)
    serviceName = models.CharField(max_length=255)

class Tenant(Nominal):
    companyName = models.CharField(max_length=255)
    services = models.ForeignKey(Services, default=1, on_delete=models.PROTECT)
    lease = models.CharField(max_length=40, blank=True, null=True, verbose_name='Lease Agreement')
    base = models.DecimalField(max_digits=11, decimal_places=2, default=0, verbose_name='Base Sales')
    salesLimit1 = models.DecimalField(max_digits=9, decimal_places=0, default=0, verbose_name='First Sales Threshold')
    percentage1 = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Percentage1')
    salesLimit2 = models.DecimalField(max_digits=9, decimal_places=0, default=0, verbose_name='Second Sales Threshold')
    percentage2 = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Percentage2')
    salesLimit3 = models.DecimalField(max_digits=9, decimal_places=0, default=0, verbose_name='Third Sales Threshold')
    percentage3 = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Percentage3')
    

    def _get_fullName(self):
         return '%s, %s %s' % (self.lastname, self.firstname, self.middlename)
    tenantName = property(_get_fullName)
    def _get_age(self):
        if self.dateBirth:
            return timezone.now().year - self.dateBirth.year
    tenantAge = property(_get_age)
    addRole = property(_get_addRole)

    def __str__(self):
        return self._get_fullName()

class Contractor(models.Model):
    contractor_id = models.AutoField(primary_key=True)
    services = models.ForeignKey(Services, on_delete=models.PROTECT)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateModified = models.DateTimeField(default=timezone.now)
    companyName = models.CharField(max_length=255, verbose_name='Company Name')
    companyNumber = models.CharField(default='999-9999', max_length=8, verbose_name='Company number')
    companyPhone = PhoneNumberField(unique=True, null=True, blank=True, verbose_name='Contact number')
    contactL1 = models.ForeignKey(Nominal, null=True, blank=True, related_name='+', verbose_name='Level 1 Contact', on_delete=models.PROTECT)
    contactL2 = models.ForeignKey(Nominal, null=True, blank=True, related_name='+', verbose_name='Level 2 Contact', on_delete=models.PROTECT)
    contactL3 = models.ForeignKey(Nominal, null=True, blank=True, related_name='+', verbose_name='Level 3 Contact', on_delete=models.PROTECT)

    # addRole = property(_get_addRole)

    class Meta:
        ordering=['companyName']

    def __str__(self):
        return self.companyName+" "+contactL1

class Personnel(Nominal):
    contractor = models.ForeignKey(Contractor, on_delete=models.RESTRICT)
    services = models.ForeignKey(Services, on_delete=models.PROTECT)
    dateStart = models.DateTimeField(default=timezone.now, verbose_name='job/contract start date')
    dateModified = models.DateTimeField(default=timezone.now)
    addRole = property(_get_addRole)

    class Meta:
        ordering=['dateStart']

    def __str__(self):
        return self.addRole








