from django.urls import URLPattern, path
from . import views

# URLconf
urlpatterns = [
    path('tenant_query/', views.query_tenant)
]