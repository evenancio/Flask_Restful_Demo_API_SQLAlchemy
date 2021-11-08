import sqlite3
import json
from flask_restful import Resource, reqparse
from flask_jwt import current_identity, jwt_required
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be empty")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be empty")

    @jwt_required()
    def get(self):
        print(json.dumps(current_identity.__dict__))
        return {'username': current_identity.username}

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201
