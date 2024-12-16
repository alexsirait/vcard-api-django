from django.urls import path

from . import views

urlpatterns = [
    path('generate_vcard', views.generate_vcard, name='generate_vcard'),
    path('chart_monthly/<str:vcard_uuid>', views.chart_monthly, name='chart_monthly'),
    path('chart_daily/<str:vcard_uuid>', views.chart_daily, name='chart_daily'),
    path('chart_location/<str:vcard_uuid>', views.chart_location, name='chart_location'),
    path('chart_total_qty/<str:vcard_uuid>', views.chart_total_qty, name='chart_total_qty'),
    path('pie_chart/<str:vcard_uuid>', views.pie_chart, name='pie_chart'),
]   