from django.core.exceptions import ObjectDoesNotExist
# from . models import Services

def _get_addRole(self):
    try:
        service = Services.objects.get(services_id=self.services_id)
        return service.serviceName
    except ObjectDoesNotExist:
        return 'service not specified'
#   addRole = property(_get_addRole)
