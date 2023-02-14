from flask_restful import Api
from flask import Flask
from Getters import GetUser, Empty
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/testDocs/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/test/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

# api.add_resource(GetUser, "/user-profile", "/user-profile/", "/user-profile/")
api.add_resource(Empty, "/empty", "/empty/")
# docs.register(GetUser)
docs.register(Empty)

if __name__ == '__main__':
    app.run(debug=True)