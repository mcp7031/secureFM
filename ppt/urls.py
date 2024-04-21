from django.urls import URLPattern, path
from . import views

# URLconf
urlpatterns = [
    path('company/', views.QueryAllCompany.as_view()),
    path('company/<int:pid>/', views.QueryCompany.as_view()),
    path('costCentre/', views.QueryAllCostCentres.as_view()),
    path('costCentre/<int:pid>/', views.QueryCostCentres.as_view()),
    path('tenant/', views.QueryAllTenantDocuments.as_view()),
    path('tenant/<int:pid>/', views.QueryTenantDocuments.as_view()),
    path('personnel/', views.QueryAllPersonnel.as_view()),
    path('personnel/<int:pid>/', views.QueryPersonnel.as_view()),
    path('locationBIMM/', views.QueryAllLocationsBIMM.as_view()),
    path('locationBIMM/<int:pid>/', views.QueryLocationBIMM.as_view()),
    path('location/', views.QueryAllLocations.as_view()),
    path('location/<int:pid>/', views.QueryLocation.as_view()),
    path('bimm/', views.QueryAllBIMM.as_view()),
    path('bimm/<int:pid>/', views.QueryBIMM.as_view()),
]
