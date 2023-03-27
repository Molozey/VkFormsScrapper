from flask_restful import Resource, reqparse, request
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from .DbGetRequestPipeline import get_request
from ApiService.SQL_pipelines import select_form_by_id, select_form_answers_by_system_id


class ResponseFormProfile(Schema):
    form_id = fields.Integer(required=True, description="Form system ID")
    vk_form_id = fields.Integer(required=True, description="Form VK ID")
    form_vk_created_date = fields.String(required=True, description="When form was created")
    form_scrapped_date = fields.String(required=True, description="When form was scrapped")
    multiple_answers = fields.String(required=True, description="Multiple answer choice available")
    form_content = fields.String(required=True, description="Form header")


class AwesomeRequestSchema(Schema):
    form_id = fields.Integer(required=True, description="Search form information by form id")


class GetFormInformation(MethodResource, Resource):
    @marshal_with(ResponseFormProfile)
    @use_kwargs(AwesomeRequestSchema, location=('query'))
    def get(self, form_id):
        """
        Get user
        :param form_id:
        :return:
        """
        # from ApiService.TestFlask import db
        form = get_request(query=select_form_by_id(system_form_id=form_id))
        content = {
            'form_id': form[0],
            'vk_form_id': form[1],
            'form_vk_created_date': form[2],
            'form_scrapped_date': form[3],
            'multiple_answers': form[4],
            'form_content': form[5],
        }
        return content, 200

    def post(self, form_id):
        return "", 201


class ResponseFormWithAnswers(Schema):
    form_id = fields.Integer(required=True, description="Form system ID")
    form_vk_created_date = fields.String(required=True, description="When form was created")
    multiple_answers = fields.String(required=True, description="Multiple answer choice available")
    form_content = fields.String(required=True, description="Form header")
    number_of_answers = fields.Integer(required=True, description="Number of form answers")
    answers = fields.List(fields.String(required=True), description="List of forms answers")


class GetComplexForm(MethodResource, Resource):
    @marshal_with(ResponseFormWithAnswers)
    @use_kwargs(AwesomeRequestSchema, location=('query'))
    def get(self, form_id):
        form = get_request(query=select_form_by_id(system_form_id=form_id))
        content = {
            'form_id': form[0],
            'form_vk_created_date': form[2],
            'multiple_answers': form[4],
            'form_content': form[5],
        }
        form_questions = get_request(query=select_form_answers_by_system_id(system_form_id=form_id), execute_many=True)
        content["number_of_answers"] = len(form_questions)
        content["answers"] = [obj[4] for obj in form_questions]
        return content, 200
