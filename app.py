from flask import Flask, request, jsonify, has_request_context
from flask.logging import default_handler
import logging
from flask_restful import Resource, Api, fields
from flask_restful_swagger import swagger


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)

app = Flask(__name__)

from modules.tax_calculator import TaxCalculator

# app = dash.Dash(server=server)
api = swagger.docs(Api(app), apiVersion='0.1')
app.logger.addHandler(default_handler)


class TaxApi(Resource):
    @swagger.operation(
        notes='This calculate the UK Tax for specific salary',
        parameters=[
            {
                "name": "salary",
                "description": "salary for the calculation of tax",
                "required": True,
                "allowMultiple": False,
                "dataType": "float",
                "paramType": "query"
            },
            {
                "name": "details",
                "description": "more details about calculation",
                "required": False,
                "allowMultiple": False,
                "dataType": "bool",
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Json results generated"
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def get(self):
        salary = float(request.args.get('salary', 0))
        details = request.args.get('details', '')
        country = request.args.get('country', 'uk')
        tax_calculator = TaxCalculator(country)

        return tax_calculator.generate(salary, True if details is not '' else False)


api.add_resource(TaxApi, '/tax-api/')

