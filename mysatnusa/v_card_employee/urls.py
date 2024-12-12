from django.urls import path

from . import views

urlpatterns = [
    path('list_vcard', views.list_vcard, name='list_vcard'),
    path('insert_vcard', views.insert_vcard, name='insert_vcard'),
    path('update_vcard/<str:vcard_uuid>', views.update_vcard, name='update_vcard'),
    # path('delete_vcard/<str:vcard_uuid>', views.delete_vcard, name='delete_vcard'),
]   



