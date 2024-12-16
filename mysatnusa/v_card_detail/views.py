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
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from operator import itemgetter

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

@jwtRequired
@csrf_exempt
def list_social_media(request, vcard_uuid):
    try:
        validate_method(request, "GET")
        with transaction.atomic():
            vcard_id = get_value(table_name="vcard.vcards",filters={'vcard_uuid':vcard_uuid},column_name='vcard_id', type="UUID")
            social_media = execute_query(
                sql_query= 
                """
                SELECT 
                vcm.*, 
                cm.*
                FROM master.contact_media vcm
                LEFT JOIN vcard.contact_media cm 
                    ON cm.vcard_id = %s AND cm.contact_media_name = vcm.contact_media_name;
                """,
                params=(vcard_id,)
            )

            return Response.ok(data=social_media, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def update_social_media(request, contact_media_uuid):
    try:
        validate_method(request, "PUT")
        with transaction.atomic():
            json_data = json.loads(request.body)
            contact_media_id = get_value(table_name="vcard.contact_media",filters={'contact_media_uuid':contact_media_uuid},column_name='contact_media_id')
            vcard_id = get_value(table_name="vcard.contact_media",filters={'contact_media_id':contact_media_id},column_name='vcard_id')
            update_data(
                table_name="vcard.contact_media",
                data={
                    "contact_media_number": json_data['contact_media_number'],
                    "contact_media_link": json_data['contact_media_link'],
                },
                filters={"contact_media_id": contact_media_id, "vcard_id": vcard_id}
            )

            return Response.ok(data=contact_media_uuid, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")
    
@jwtRequired
@csrf_exempt
def delete_social_media(request, contact_media_uuid):
    try:
        validate_method(request, "DELETE")
        with transaction.atomic():
            contact_media_id = get_value(table_name="vcard.contact_media",filters={'contact_media_uuid':contact_media_uuid},column_name='contact_media_id')
            delete_data(
                table_name="vcard.contact_media",
                filters={
                    "contact_media_id": contact_media_id
                }
            )

            return Response.ok(data=contact_media_uuid, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")