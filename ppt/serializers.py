from rest_framework import serializers
from .models import Tenant

class TenantSerializer(serializers.Serializer):
    class Meta:
        model=Tenant
        fields=('age')
        