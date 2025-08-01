from django.urls import path
from .views import home, report_api

urlpatterns = [
    path('', home, name='home'),
    path('api/report/', report_api, name='report_api'),
]
