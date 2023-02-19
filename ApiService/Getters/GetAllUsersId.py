from flask_restful import Resource, reqparse, request
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from ApiService.SQL_pipelines import select_user_by_id


class ResponseAllUsersId(Schema):
    users_ids = fields.List(cls_or_instance=fields.Integer, description="All users ids")


# class AwesomeRequestSchema(Schema):
#     nothing = fields.Integer(required=True, description="nothing")
# http://127.0.0.1:5000/user-profile/?user_id=0&user_name=al


class GetAllUsersId(MethodResource, Resource):
    @marshal_with(ResponseAllUsersId)
    # @use_kwargs(AwesomeRequestSchema, location='query')
    def get(self):
        """
        Get user
        :param user_id:
        :return:
        """
        from ApiService.TestFlask import db

        users_ids = db.mysql_get_execution_handler("SELECT user_id FROM USER_TABLE", multi=True)

        content = {
            'users_ids': [ids[0] for ids in users_ids]
        }
        return content, 200


    def post(self):
        return "", 201