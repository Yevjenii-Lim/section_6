import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="give your username")
    parser.add_argument("password", type=str, required=True, help="give your password")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message":f"user with name {data['username']} is alredy exists"} , 400

        user = UserModel(**data)
        user.save_user_to_db()
        # UserModel.save_user_to_db()
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO users VALUES(NULL, ?, ?)"
        # cursor.execute(query, (data["username"], data["password"]))

        # connection.commit()
        # connection.close()

        return {"message": "user created suceseful"}, 201

    def get(self):
        return {"all users": [user.json() for user in UserModel.query.all()]} 

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        select_query = "SELECT * from users"
        result = []

        for row in cursor.execute(select_query):
            user = User(*row).json()
            result.append(user)

        return {"all users": result}, 201

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
    def json(self):
        return {"id": self.id, "name": self.name, "password": self.password}
