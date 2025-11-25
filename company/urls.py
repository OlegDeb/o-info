from django.urls import path
from .views import *
 

urlpatterns = [
    path('par/', par, name='par'),
    path('form_company/', form_company, name='form_company'),
]