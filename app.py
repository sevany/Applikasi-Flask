from os import name
from flask import Flask, request
from werkzeug.wrappers import response
from flask_restful import Resource, Api
from flask_cors import CORS

#inisiasi object

app = Flask(__name__)

api = Api(app)


CORS(app)

identiti = {} #dictionary =json

class ContohResource(Resource):
    def get(self):
        # response = {"msg": "Hallo dunia yang memenatkan"}
        # return response
        return identiti

    def post(self):
        name = request.form["name"]
        age = request.form["age"]
        company = request.form["company_name"]
        identiti["name"] = name
        identiti["age"] = age
        identiti["company"] = company
        response = {"msg": "Data dah masuk"}
        return response



##setup resource 
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])


if __name__ == "__main__":
    app.run (debug=True, port=5005)
