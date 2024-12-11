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
def list_setting_cargo_lift(request):
    try:
        validate_method(request, "GET")
        with transaction.atomic():
            search = request.GET.get('search', '')
            department = request.GET.get('department', '')
            linecode = request.GET.get('linecode', '')

            filter_box={}
            
            if department:
                filter_box['department_name'] = department 
            if linecode:
                filter_box['line_code'] = linecode

            list_setting_cargo = get_data(table_name='cargo_lift.v_cargo_lift_user',filters=filter_box, search=search, search_columns=['employee_name', 'employee_badge', 'department_name', 'line_code', 'cargo_lift_user_description'])
            paginate = paginate_data(request, list_setting_cargo)

            return Response.ok(data=paginate, message="List data telah tampil", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def insert_setting_cargo_lift(request):
    try:
        validate_method(request, "POST")
        with transaction.atomic():
            json_data = json.loads(request.body)
            rules = {
                'employee_name': 'required|string|min:3|max:255',
                'employee_badge': 'required|string|min:3|max:10',
                'department_name': 'required|string|min:3|max:255',
                'department_code': 'required|string|min:3|max:10',
                'line_code': 'required|string|min:3|max:255',
                'description': 'required|string',
            }

            validation_errors = validate_request(json_data, rules)
            if validation_errors:
                return Response.badRequest(request, message=validation_errors, messagetype="E")

            cargo_id = insert_get_id_data(
                table_name="cargo_lift.cargo_lift_users",
                data={
                    "employee_name": json_data['employee_name'],
                    "employee_badge": json_data['employee_badge'],
                    "department_name": json_data['department_name'],
                    "department_code": json_data['department_code'],
                    "line_code": json_data['line_code'],
                    "cargo_lift_user_description": json_data['description'],
                },
                column_id = "cargo_lift_user_id" 
            )

            delete_data(table_name="cargo_lift.cargo_lift_assigns",filters={"cargo_lift_user_id": cargo_id})
            for i in json_data['cargo_assigns']:
                insert_data(
                    table_name="cargo_lift.cargo_lift_assigns", 
                    data={
                        "cargo_lift_id": i,
                        "cargo_lift_user_id": cargo_id,
                    },
                )
                            
            return Response.ok(data={"cargo_lift_uuid" : cargo_id}, message="Added!", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")

@jwtRequired
@csrf_exempt
def update_setting_cargo_lift(request, cargo_uuid):
    try:
        validate_method(request, "PUT")
        with transaction.atomic():
            json_data = json.loads(request.body)
            rules = {
                'description': 'required|string',
            }

            validation_errors = validate_request(json_data, rules)
            if validation_errors:
                return Response.badRequest(request, message=validation_errors, messagetype="E")

            cargo_lift_user_id = get_value(table_name="cargo_lift.cargo_lift_users", filters={"cargo_lift_user_uuid": cargo_uuid} ,column_name="cargo_lift_user_id", type='UUID')

            cargo_id = update_data(
                table_name="cargo_lift.cargo_lift_users",
                data={
                    "cargo_lift_user_description": json_data['description'],
                },
                filters={
                    "cargo_lift_user_id": cargo_lift_user_id,
                }
            )

            delete_data(table_name="cargo_lift.cargo_lift_assigns",filters={"cargo_lift_user_id": cargo_lift_user_id})

            for i in json_data['cargo_assigns']:
                insert_data(
                    table_name="cargo_lift.cargo_lift_assigns", 
                    data={
                        "cargo_lift_id": i,
                        "cargo_lift_user_id": cargo_lift_user_id,
                    },
                )
                            
            return Response.ok(data={"cargo_lift_uuid" : cargo_uuid}, message="Updated!", messagetype="S")
    except Exception as e:
        return Response.badRequest(request, message=str(e), messagetype="E")


@jwtRequired
@csrf_exempt
def delete_setting_cargo_uuid(request, cargo_uuid):
    try:
        validate_method(request, "DELETE")
        with transaction.atomic():
            cargo_lift_user_id = get_value(table_name="cargo_lift.cargo_lift_users", filters={"cargo_lift_user_uuid": cargo_uuid} ,column_name="cargo_lift_user_id", type='UUID')

            delete_data(
                table_name="cargo_lift.cargo_lift_users",
                filters={"cargo_lift_user_id": cargo_lift_user_id},
            )

            delete_data(
                table_name="cargo_lift.cargo_lift_assigns",
                filters={"cargo_lift_user_id": cargo_lift_user_id},
            )

            return Response.ok(data={"cargo_lift_uuid": cargo_uuid}, message="Deleted!", messagetype="S")
    except Exception as e:
        log_exception(request, e)
        return Response.badRequest(request, message=str(e), messagetype="E")
