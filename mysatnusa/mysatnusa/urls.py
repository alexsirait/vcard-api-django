from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from mysatnusa.response import Response

schema_view = get_schema_view(
   openapi.Info(
      title="My satnusa platform",
      default_version='v1',
      description="API description",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', lambda r: Response.ok(message="Service Running ..")),
    path('api/v_card_report/', include('v_card_report.urls')),
    path('api/v_card_employee/', include('v_card_employee.urls')),
    path('api/v_card_detail/', include('v_card_detail.urls'))
]