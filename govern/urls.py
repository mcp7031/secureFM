from django.urls import URLPattern, path
from . import views

# URLconf
urlpatterns = [
    path('govern_query/', views.query_govern)
]