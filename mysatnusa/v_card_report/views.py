import json
from django.db import connection, transaction
from mysatnusa.response import Response
from django.views.decorators.csrf import csrf_exempt
from mysatnusa.middleware import jwtRequired
from django.core.paginator import Paginator
from django.urls import reverse
from common.pagination_helper import paginate_data
from common.transaction_helper import *
import datetime
import environ
import jwt
import os
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from operator import itemgetter
import base64

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

@csrf_exempt
def generate_vcard(request):
    try:
        validate_method(request, "GET")
        
        full_name = "Alex Sirait"
        first_name = "Alex"
        last_name = "Sirait"
        email = "SirAyek@example.com"
        org = "PT. SAT NUSAPERSADA Tbk"
        title = "Legal & Investor Relation"
        adr = ";;Jl. Pelita VI No.99;Batam;Kepulauan Riau;29443;Indonesia"
        work_phone = "+62 778 570 8888"
        cell_phone = "+62 852 6460 6070"
        fax_phone = ""
        work_email = "SirAyek@example.com"
        url = "https://www.example.com/"

        photo_filename = "tes.jpg"
        photo_path = os.path.join(settings.MEDIA_ROOT, 'uploads', photo_filename)

        if not os.path.exists(photo_path):
            return Response.badRequest(request, message="Photo not found", messagetype="E")

        with open(photo_path, "rb") as photo_file:
            photo_data = photo_file.read()
            photo_base64 = base64.b64encode(photo_data).decode("utf-8")

        vcard_content = f"""
            BEGIN:VCARD
            VERSION:3.0
            FN:{full_name}
            N:{last_name};{first_name};;;
            EMAIL:{email}
            ORG:{org}
            TITLE:{title}
            ADR:{adr}
            TEL;WORK;VOICE:{work_phone}
            TEL;CELL:{cell_phone}
            TEL;FAX:{fax_phone}
            EMAIL;WORK;INTERNET:{work_email}
            URL:{url}
            PHOTO;ENCODING=BASE64;TYPE=JPEG:{photo_base64}
            END:VCARD
        """
        response = HttpResponse(vcard_content, content_type="text/vcard")
        response['Content-Disposition'] = f'attachment; filename="{full_name}.vcf"'
        return response

    except FileNotFoundError as e:
        return Response.badRequest(request, message=f"File not found: {str(e)}", messagetype="E")
    except Exception as e:
        log_exception(request, e)
        return Response.badRequest(request, message=f"An error occurred: {str(e)}", messagetype="E")
    
@jwtRequired
@csrf_exempt
def chart_monthly(request, vcard_uuid):
    try:
        validate_method(request, "GET")
        with transaction.atomic():

            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            
            chart_monthly = execute_query(
                            sql_query=
                            """
                            SELECT * FROM vcard.chart_monthly(%s, %s, %s);
                            """,
                            params=(vcard_uuid, start_date, end_date,)
                        )
            return Response.ok(data=chart_monthly, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def chart_daily(request, vcard_uuid):
    try:
        validate_method(request, "GET")
        with transaction.atomic():

            year = request.GET.get('year', '')
            month = request.GET.get('month', '')
            
            chart_daily = execute_query(
                            sql_query=
                            """
                            SELECT * FROM vcard.chart_daily(%s, %s, %s);
                            """,
                            params=(vcard_uuid, year, month,)
                        )
            return Response.ok(data=chart_daily, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def chart_location(request, vcard_uuid):
    try:
        validate_method(request, "GET")
        with transaction.atomic():

            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            
            chart_location = execute_query(
                            sql_query=
                            """
                            SELECT * FROM vcard.chart_location(%s, %s, %s);
                            """,
                            params=(vcard_uuid, start_date, end_date,)
                        )
            return Response.ok(data=chart_location, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def chart_total_qty(request, vcard_uuid):
    try:
        validate_method(request, "GET")
        with transaction.atomic():

            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            
            chart_total_qty = execute_query(
                            sql_query=
                            """
                            SELECT * FROM vcard.total_scan(%s, %s, %s);
                            """,
                            params=(vcard_uuid, start_date, end_date,)
                        )
            return Response.ok(data=chart_total_qty, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def pie_chart(request, vcard_uuid):
    try:
        validate_method(request, "GET")
        with transaction.atomic():

            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            
            pie_chart = execute_query(
                            sql_query=
                            """
                            SELECT * FROM vcard.chart_event(%s, %s, %s);
                            """,
                            params=(vcard_uuid, start_date, end_date,)
                        )
            return Response.ok(data=pie_chart, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")