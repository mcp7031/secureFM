from django.contrib import admin
from . import models
from ppt.models import Nominal
from ppt.models import Company

# Register your models here.
@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ('tradeName', 'compName', 'account')
    list_display = ['tradeName', 'account']

admin.site.register(models.CostCentre)
admin.site.register(models.Location)
admin.site.register(models.Nominal)


