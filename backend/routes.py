from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for i in data:
        if i["id"]==id:
            return jsonify(i), 200
    return {"message": "picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # get data from the json body
    picture_in = request.json
    for i in data:
        if i["id"]==picture_in["id"]:
            return {"Message": "picture with id {id} already present".format(id=picture_in["id"])}, 302
    data.append(picture_in)
    response = app.response_class(
        response=json.dumps(picture_in),
        status=201,
        mimetype='application/json'
    )
    return response

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    for i in data:
        if i["id"]==id:
            data[data.index(i)]=request.json
            return {"message":"updated"}, 200
    return {"message": "picture not found"}, 404  

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in data:
        if i["id"]==id:
            data.remove(i)
            return {"message":""}, 204
    return {"message": "picture not found"}, 404  
