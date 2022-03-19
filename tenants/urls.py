from django.urls import URLPattern, path
from . import views

# URLconf
urlpatterns = [
    path('tenant/', views.query_tenant)
]
