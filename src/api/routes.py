"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

api = Blueprint('api', __name__)

@api.route('/singup', methods=['POST'])
def create_user():
    body = request.get_json()
    hashed = bcrypt.hashpw(body['password'].encode(),bcrypt.gensalt(14))#de
    new_user=User(body['email'],hashed.decode()) #de byte a string
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@api.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.query.filter_by(email=body['email']).one()
    if bcrypt.checkpw(body['password'].encode(), user.password.encode()):
        access_token = create_access_token(identity=user.serialize())
        return jsonify(access_token),200
    else:
        return jsonify("It Does not Match :("),403

@api.route("/private", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200