from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def query_tenant(request):
    x = 1
    y = 2
#  return HttpResponse('return from query_tenant function')
    return render(request, 'tenant.html', {'name' : 'David'})
