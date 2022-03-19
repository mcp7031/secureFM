from django.db import models

# Create your models here.

class Tenant(models.Model):
    tenant_id = models.AutoField(primary_key=True)
    lastName = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    companyName = models.CharField(max_length=255)

