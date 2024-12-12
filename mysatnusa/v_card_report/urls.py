from django.urls import path

from . import views

urlpatterns = [
    path('generate_vcard', views.generate_vcard, name='generate_vcard'),
]   