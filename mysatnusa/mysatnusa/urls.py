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
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   #  path('admin/', admin.site.urls),
    path('', lambda r: Response.ok(message="Service Running ..")),
   #  path('api/cargo_lift/', include('cargo_lift.urls')),
   #  path('api/setting_module_cargo_lift/', include('setting_module_cargo_lift.urls')),
]