from django.urls import path

from . import views

urlpatterns = [
    path('list_vcard', views.list_vcard, name='list_vcard'),
    path('list_event/<str:vcard_uuid>', views.list_event, name='list_event'),
    path('detail_event/<str:event_uuid>', views.detail_event, name='detail_event'),
    path('insert_vcard', views.insert_vcard, name='insert_vcard'),
    path('update_vcard/<str:vcard_uuid>', views.update_vcard, name='update_vcard'),
    # path('delete_vcard/<str:vcard_uuid>', views.delete_vcard, name='delete_vcard'),
]   



