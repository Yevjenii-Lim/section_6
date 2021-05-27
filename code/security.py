from werkzeug.security import safe_str_cmp
from models.user import UserModel
# from resources.user import User

#
# username_mapping = {u.name : u for u in users}
#
# userid_mapping = {u.id : u for u in users}

userpassword_mapping = {
    "qwer" : {    "id": 1,
            "name": "bob",
            "password": "qwer"
            }
}

def authenticate(username, password):
    user = UserModel.find_by_username(username)

    if user and safe_str_cmp(user.password , password):
        return user

def identity(playload):
    user_id = playload["identity"]
    return UserModel.find_by_id(user_id)
