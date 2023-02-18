from flask_restful import Resource, reqparse, request
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from ApiService.SQL_pipelines import select_user_by_id


class ResponseUserProfile(Schema):
    user_id = fields.Integer(required=True, description="User system ID")
    vk_user_id = fields.Integer(required=True, description="User VK ID")
    user_vk_profile_url = fields.String(required=True, description="User VK profile logo URL")
    user_first_name = fields.String(required=True)
    user_sec_name = fields.String(required=True)
    user_sex = fields.String(required=True)
    user_birth_date = fields.String(required=True)
    user_city = fields.String(required=True)
    user_country = fields.String(required=True)
    user_job_place = fields.String(required=True)
    user_education_place = fields.String(required=True)
    user_number_of_friends = fields.String(required=True)
    user_status = fields.String(required=True)


class AwesomeRequestSchema(Schema):
    user_id = fields.Integer(required=True, description="Search user profile by id")
# http://127.0.0.1:5000/user-profile/?user_id=0&user_name=al


class GetUserProfile(MethodResource, Resource):
    @marshal_with(ResponseUserProfile)
    @use_kwargs(AwesomeRequestSchema, location=('query'))
    def get(self, user_id):
        """
        Get user
        :param user_id:
        :return:
        """
        from ApiService.TestFlask import db

        user = db.mysql_get_execution_handler(select_user_by_id(system_user_id=user_id))
        content = {
            'user_id': user[0],
            'vk_user_id': user[1],
            'user_vk_profile_url': user[2],
            'user_first_name': user[3],
            'user_sec_name': user[4],
            'user_sex': user[5],
            'user_birth_date': user[6],
            'user_city': user[7],
            'user_country': user[8],
            'user_job_place': user[9],
            'user_education_place': user[10],
            'user_number_of_friends': user[11],
            'user_status': user[12],

        }
        return content, 200


    def post(self, user_id):
        return "", 201