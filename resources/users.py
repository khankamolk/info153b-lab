import os
import requests
from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import UserRegisterSchema, UserSchema
from models import UserModel
from sqlalchemy import or_

from tasks import send_user_registration_email


blp = Blueprint("users", __name__, description="User APIs")

@blp.route("/registerqueue")
class UserRegisterWithQueue(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"],
            )
        ).first():
            abort(409, message="A user with that username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        db.session.add(user)
        db.session.commit()
        
        # go to the current app's queue (which is stored in app.py) and push the send_user_registration_email function to it 
        # the following two arguments are arguments to the send_user_registration_email function
        current_app.queue.enqueue(send_user_registration_email, user.email, user.username)
        # mail will be sent when the background worker picks it up.

        return {"message": "User created successfully."}, 201
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
    
@blp.route("/users")
class Users(MethodView):
    @blp.response(200, UserSchema(many=True)) 
    def get(self):
        return UserModel.query.all()
