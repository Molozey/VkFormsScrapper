from flask_restful import Resource, reqparse, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields


class AwesomeRequestSchema(Schema):
    user_id = fields.String(required=True, description="User id")
    user_name = fields.String(required=True, default="User name")

# http://127.0.0.1:5000/user-profile/?user_id=0&user_name=al


class GetUser(MethodResource, Resource):
    @use_kwargs(AwesomeRequestSchema)
    def get(self):
        """
        Get user
        :param user_id:
        :return:
        """
        user_id = request.args.get('user_id', "")
        user_name = request.args.get('user_name', "")
        print(user_id, user_name)
        if int(user_id) != 0:
            return "Quote not found", 404
        else:
            return {"user": f"{user_name}",
                    "sex": "male",
                    "user_id": f"{user_id}"
                    }, 200

    def post(self, user_id):
        """
        Post new user
        :param user_id:
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        params = parser.parse_args()
        quote = {
            "id": int(user_id),
            "author": params["author"],
            "quote": params["quote"]
        }
        print("Add quote:", quote)
        return quote, 201