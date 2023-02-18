from flask_restful import Api
from flask import Flask
from Getters import GetUserProfile
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from MySQLGetter import MySqlDaemon
import yaml

global db

# Record system
try:
    with open("getting_info/configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
except FileNotFoundError:
    with open("configuration.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
db = MySqlDaemon(config=cfg)

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

# TODO: Add resources here
api.add_resource(GetUserProfile, "/empty", methods=['GET'])
docs.register(GetUserProfile)

if __name__ == '__main__':
    app.run(debug=True)