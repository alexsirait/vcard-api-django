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
#swagger
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from .serializers import *  # Import the serializer
# from .utils.serializer_helper import SerializerHelper
# from .utils.serializer_helper import swagger_post_scheme
#end swagger
from operator import itemgetter

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()


@jwtRequired
@csrf_exempt
def list_vcard(request):
    try:
        validate_method(request, "GET")
        with transaction.atomic():
            search = request.GET.get('search', '').lower()
            department_name = request.GET.get('department_name', '').lower()  # Pastikan menggunakan .lower() untuk pencarian case-insensitive
            line_code = request.GET.get('line_code', '').lower()
            position = request.GET.get('position_name', '')
            
            filter_box = {}
            
            if position :
                filter_box['position_name'] = position
            
            list_vcard = get_data(table_name='vcard.vcards',filters=filter_box)
            
            data = []
            for item in list_vcard:
                data.append({
                    **item,
                    "department_name": get_value(table_name='master.v_employee',filters={'employee_badge':item['employee_badge']},column_name='department_name'),
                    "department_code": get_value(table_name='master.v_employee',filters={'employee_badge':item['employee_badge']},column_name='department_code'),
                    "line_code": get_value(table_name='master.v_employee',filters={'employee_badge':item['employee_badge']},column_name='line_code')
                })
            
            if search or department_name or line_code:
                data = [
                    item for item in data
                    if (not search or (
                            search in item.get('employee_name', '').lower() or
                            search in item.get('department_name', '').lower() or
                            search in item.get('line_code', '').lower() or
                            search in item.get('employee_badge', '').lower()
                    )) and
                    (not department_name or department_name in item.get('department_name', '').lower()) and
                    (not line_code or line_code in item.get('line_code', '').lower())
                ] 
            
            paginate = paginate_data(request, data)

            return Response.ok(data=paginate, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def insert_vcard(request):
    try:
        validate_method(request, "POST")
        with transaction.atomic():
            json_data = json.loads(request.body)
            rules = {
                'employee_name': 'required|string|min:3|max:255',
                'employee_badge': 'required|string|min:3|max:10',
                'is_active': 'required|boolean',
            }

            validation_errors = validate_request(json_data, rules)
            if validation_errors:
                return Response.badRequest(request, message=validation_errors, messagetype="E")

            vcard_id = insert_get_id_data(
                table_name="vcard.vcards",
                data={
                    "employee_name": json_data['employee_name'],
                    "employee_badge": json_data['employee_badge'],
                    "is_active": json_data['is_active'],
                    "position_name": json_data['position_name'],
                    "created_at": datetime.datetime.now(),
                    "created_by": request.jwt_badge_no,
                    "created_by_name": request.jwt_fullname,
                    "updated_at": datetime.datetime.now(),
                    "updated_by": request.jwt_badge_no,
                    "updated_by_name": request.jwt_fullname,
                },
                column_id = "vcard_id" 
            )

            # delete_data(table_name="cargo_lift.cargo_lift_assigns",filters={"cargo_lift_user_id": vcard_id})
            # for i in json_data['cargo_assigns']:
            #     insert_data(
            #         table_name="cargo_lift.cargo_lift_assigns", 
            #         data={
            #             "cargo_lift_id": i,
            #             "cargo_lift_user_id": cargo_id,
            #         },
            #     )
            
            vcard_uuid = get_value(table_name='vcard.vcards',filters={'vcard_id':vcard_id},column_name='vcard_uuid')
                            
            return Response.ok(data={"vcard_uuid" : vcard_uuid}, message="Added!", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def update_vcard(request, vcard_uuid):
    try:
        validate_method(request, "PUT")
        with transaction.atomic():
            json_data = json.loads(request.body)
            rules = {
                'employee_name': 'required|string|min:3|max:255',
                'employee_badge': 'required|string|min:3|max:10',
                'is_active': 'required|boolean',
            }

            validation_errors = validate_request(json_data, rules)
            if validation_errors:
                return Response.badRequest(request, message=validation_errors, messagetype="E")

            vcard_id = get_value(table_name="vcard.vcards", filters={"vcard_uuid": vcard_uuid} ,column_name="vcard_id", type='UUID')

            update_data(
                table_name="vcard.vcards",
                data={
                    "employee_name": json_data['employee_name'],
                    "employee_badge": json_data['employee_badge'],
                    "is_active": json_data['is_active'],
                    "position_name": json_data['position_name'],
                },
                filters={
                    "vcard_id": vcard_id,
                }
            )
                            
            return Response.ok(data={"vcard_uuid" : vcard_uuid}, message="Updated!", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")


# @jwtRequired
# @csrf_exempt
# def delete_vcard(request, vcard_uuid):
#     try:
#         validate_method(request, "DELETE")
#         with transaction.atomic():
#             cargo_lift_user_id = get_value(table_name="cargo_lift.cargo_lift_users", filters={"cargo_lift_user_uuid": vcard_uuid} ,column_name="cargo_lift_user_id", type='UUID')

#             delete_data(
#                 table_name="cargo_lift.cargo_lift_users",
#                 filters={"cargo_lift_user_id": cargo_lift_user_id},
#             )

#             delete_data(
#                 table_name="cargo_lift.cargo_lift_assigns",
#                 filters={"cargo_lift_user_id": cargo_lift_user_id},
#             )

#             return Response.ok(data={"cargo_lift_uuid": vcard_uuid}, message="Deleted!", messagetype="S")
#     except Exception as e:
#         log_exception(request, e)
#         return Response.badRequest(request, message=str(e), messagetype="E")
