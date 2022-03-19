from pyexpat import model
from ppt.utils import _get_addRole
from operator import mod
from django.contrib.auth import get_user_model
from django.db import models
# from django.contrib.mysql.fields import JSONField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from address.models import AddressField

# Create your models here.

class Nominal(models.Model):
    nominal_id = models.AutoField(primary_key=True)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateBirth = models.DateTimeField(verbose_name='date of birth')
    lastName = models.CharField(max_length=255, verbose_name='last name')
    firstName = models.CharField(max_length=255, verbose_name='first name')
    middleName = models.CharField(max_length=255, null=True, verbose_name='middle name')
    driverLicense = models.IntegerField(null=True, verbose_name='driver license')
    driverClass = models.CharField(max_length=4, default='C', verbose_name='class of license') 
    address1 = AddressField()
    address2 = AddressField(related_name='+', blank=True, null=True)
    

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    tradeName = models.CharField(max_length=255, verbose_name='Company Name')
    compName = models.CharField(max_length=255, verbose_name='Trade Name')
    abn = models.CharField(editable=True, max_length=8, verbose_name='ABN')
    account = models.CharField(default='999-999-9999', editable=True, max_length=12, verbose_name='G/L account number')
    contactL1 = models.ForeignKey(Nominal, null=True, related_name='+', verbose_name='Level 1 Contact', on_delete=models.PROTECT)
    contactL2 = models.ForeignKey(Nominal, null=True, related_name='+', verbose_name='Level 2 Contact', on_delete=models.PROTECT)
    contactL3 = models.ForeignKey(Nominal, null=True, related_name='+', verbose_name='Level 3 Contact', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.compName


class CostCentre(models.Model):
    costCentre_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    costName = models.CharField(max_length=255)
    costAccount = models.PositiveIntegerField
    contactL1 = models.ForeignKey(Nominal, null=True, related_name='+', on_delete=models.PROTECT)
    contactL2 = models.ForeignKey(Nominal, null=True, related_name='+', on_delete=models.PROTECT)
    contactL3 = models.ForeignKey(Nominal, null=True, related_name='+', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.costName 

class AccessGroups(models.Model):
    accessGroup_id = models.AutoField(primary_key=True)
    groupCode = models.CharField(max_length=6)
    groupName = models.CharField(max_length=255)
    accessLevel = models.IntegerField

class BIM(models.Model):
    bim_id = models.AutoField(primary_key=True)
    name = models.CharField(default='default', max_length=255)
    description = models.TextField
    mongoDB_id = models.BigIntegerField

class BIMM(models.Model):
    bimm_id = models.AutoField(primary_key=True)
    description = models.TextField
    bim =  models.ManyToManyField(BIM)

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    costCentre = models.ForeignKey(CostCentre, on_delete=models.CASCADE)
    locationCode = models.CharField(max_length=26)
    bimm = models.ManyToManyField(BIMM)

class LocationGroupAccess(models.Model):
    locationGroupAccess_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, related_name='+', on_delete=models.PROTECT)
    accessGroup = models.ForeignKey(AccessGroups, related_name='+', on_delete=models.PROTECT)

class NominalGroupAccess(models.Model):
    nominalGroupAccess_id = models.AutoField(primary_key=True)
    nominal = models.ForeignKey(Nominal, related_name='+', on_delete=models.PROTECT)
    accessGroup = models.ForeignKey(AccessGroups, related_name='+', on_delete=models.PROTECT)

class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    nominal = models.ForeignKey(Nominal, on_delete=models.CASCADE)
    mongoDB_id = models.BigIntegerField
    docName = models.CharField(max_length=255, verbose_name='name of document')
    docDesc = models.TextField

class Services(models.Model):
    services_id = models.AutoField(primary_key=True)
    serviceCode = models.CharField(max_length=6)
    serviceName = models.CharField(max_length=255)

class Tenant(Nominal):
    companyName = models.CharField(max_length=255)
    services = models.ForeignKey(Services, default=1, on_delete=models.PROTECT)

    def _get_fullName(self):
         return '%s, %s %s' % (self.lastname, self.firstname, self.middlename)
    tenantName = property(_get_fullName)
    def _get_age(self):
        if self.dateBirth:
            return timezone.now().year - self.dateBirth.year
    tenantAge = property(_get_age)
    addRole = property(_get_addRole)

class Contractor(models.Model):
    contractor_id = models.AutoField(primary_key=True)
    services = models.ForeignKey(Services, on_delete=models.PROTECT)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateModified = models.DateTimeField(default=timezone.now)
    companyName = models.CharField(max_length=255)
    companyNumber = models.IntegerField
    addRole = property(_get_addRole)

class Personnel(Nominal):
    contractor_id = models.ForeignKey(Contractor, on_delete=models.RESTRICT)
    services_id = models.ForeignKey(Services, on_delete=models.PROTECT)
    dateStart = models.DateTimeField(default=timezone.now, verbose_name='job/contract start date')
    dateModified = models.DateTimeField(default=timezone.now)
    addRole = property(_get_addRole)








