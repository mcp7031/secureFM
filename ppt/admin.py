from django.contrib import admin
from . import models
from ppt.models import Nominal
from ppt.models import Company

# Register your models here.
@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ('tradeName', 'compName', 'account')
    list_display = ['tradeName', 'account']

@admin.register(models.CostCentre)
class CostCentreAdmin(admin.ModelAdmin):
    fields=('company', 'costName', 'costAccount', 'contactL1', 'contactL2', 'contactL3')

@admin.register(models.Location)
class LocationCentreAdmin(admin.ModelAdmin):
    fields=('costCentre', 'locationCode', 'description')

@admin.register(models.Nominal)
class NominalAdmin(admin.ModelAdmin):
    fields=('costCentre', 'location', 'firstName', 'lastName', 'dateBirth', 'driverLicense', 'driverClass', 'address1')

@admin.register(models.Contractor)
class ContractorAdmin(admin.ModelAdmin):
    fields=('companyName', 'companyNumber', 'companyPhone', 'contactL1')

@admin.register(models.Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    fields=('contractor_id', 'services_id', 'dateStart')
    



