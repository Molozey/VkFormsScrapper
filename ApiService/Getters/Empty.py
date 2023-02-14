from flask_restful import Resource, reqparse, request
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields


class AwesomeRequestSchema(Schema):
    user_id = fields.String(required=True, description="User id")
    user_name = fields.String(required=True, default="User name")


class AwesomeResponseSchema(Schema):
    message = fields.Str(default='Success')

# http://127.0.0.1:5000/user-profile/?user_id=0&user_name=al


get_params = use_kwargs({'user_id': fields.Str()}, location="query")


class Empty(MethodResource, Resource):
    @marshal_with(AwesomeResponseSchema)
    @get_params
    def get(self, user_id):
        """
        Get user
        :param user_id:
        :return:
        """
        print(user_id)
        return "", 200

    def post(self, user_id):
        return "", 201