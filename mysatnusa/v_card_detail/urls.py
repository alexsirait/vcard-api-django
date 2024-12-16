from django.urls import path

from . import views

urlpatterns = [
    path('list_social_media/<str:vcard_uuid>', views.list_social_media, name='list_social_media'),
    path('update_social_media/<str:contact_media_uuid>', views.update_social_media, name='update_social_media'),
    path('delete_social_media/<str:contact_media_uuid>', views.delete_social_media, name='delete_social_media'),
]