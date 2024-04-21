from django.urls import URLPattern, path
from . import views

# URLconf
urlpatterns = [
    path('current_incidents/', views.query_current)
]