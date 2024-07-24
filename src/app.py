"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

john_jackson = {
    "first_name": "John",
    "age": "33",
    "lucky_numbers": [7, 13, 22]
}

jane_jackson = {
    "first_name": "Jane",
    "age": "35",
    "lucky_numbers": [10, 14, 3]
}

jimmy_jackson = {
    "first_name": "Jimmy",
    "last_name": "Jackson",
    "age": "5",
    "lucky_numbers": [1]
}

jackson_family.add_member(john_jackson)
jackson_family.add_member(jane_jackson)
jackson_family.add_member(jimmy_jackson)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_family_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def create_member():
    member = request.json
    print("Successfully created", member)
    jackson_family.add_member(member)
    return "Successfully created new member", 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.get_member(id)

    if member:
        jackson_family.delete_member(id)
        return "Member deleted successfully", 200
    else:
        return "Member not found", 404

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member_data = request.json
    if jackson_family.update_member(id, member_data):
        return "Member updated successfully", 200
    else:
        return "Member not found", 404

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
