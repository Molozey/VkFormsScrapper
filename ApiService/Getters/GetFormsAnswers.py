from flask_restful import Resource, reqparse, request
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from collections import OrderedDict

from ApiService.SQL_pipelines import select_forms_by_user_id, all_answers_by_form_id


class ResponseFormsAnswers(Schema):
    form_id = fields.List(required=True, cls_or_instance=fields.Integer(), description="User's system form ID")
    user_form_info = fields.List(required=True, cls_or_instance=fields.Dict(keys=fields.Str()),
                                 description="User's answers for this form")


class AwesomeRequestSchema(Schema):
    user_id = fields.Integer(required=True, description="Search user forms by id")


# http://127.0.0.1:5000/user-profile/?user_id=0&user_name=al


class GetFormsAnswers(MethodResource, Resource):
    @marshal_with(ResponseFormsAnswers)
    @use_kwargs(AwesomeRequestSchema, location='query')
    def get(self, user_id):
        """
        Get user
        :param user_id:
        :return:
        """
        from ApiService.TestFlask import db

        users_form_to_answer = OrderedDict()
        form_to_answer = db.mysql_get_execution_handler(select_forms_by_user_id(system_user_id=user_id), multi=True)
        for form_id, answer_id in form_to_answer:
            if form_id not in users_form_to_answer.keys():
                users_form_to_answer[form_id] = [answer_id]
            else:
                users_form_to_answer[form_id].append(answer_id)

        answers_arr = []
        for form_id in users_form_to_answer.keys():
            all_answers = db.mysql_get_execution_handler(all_answers_by_form_id(system_form_id=form_id), multi=True)
            answers_dict = {
                "form_id": form_id,
                "user_answers": users_form_to_answer[form_id],
                "all_form_answers": [answer[0] for answer in all_answers]
            }
            answers_arr.append(answers_dict)

        content = {
            "form_id": users_form_to_answer.keys(),
            "user_form_info": answers_arr
        }
        return content, 200

    def post(self, user_id):
        return "", 201
