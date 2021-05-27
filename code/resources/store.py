from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {"message": "store not found"}, 404

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"maessage": "message deleted"}

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message":"alredy excists"}

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "can not save"}, 500

        return store.json(), 201

class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()] }
