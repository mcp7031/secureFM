from django.urls import URLPattern, path
from . import views

# URLconf
urlpatterns = [
#    path('tenant_query/', views.query_tenant),
    path('tenant_query/', views.QueryAllTenantDocuments.as_view()),
    path('tenant_query/<int:pid>/', views.QueryTenantDocuments.as_view()),
    path('location_query/', views.QueryAllLocations.as_view()),
    path('location_query/<int:pid>/', views.QueryLocation.as_view()),
    path('bimm_query/', views.QueryAllBIMM.as_view()),
    path('bimm_query/<int:pid>/', views.QueryBIMM.as_view()),
]
