
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel, ItemsListModel

def check_items_db(name):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    query = "SELECT * FROM items WHERE name=?"
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    if row:
        return row

    return None

class Items(Resource):
    def get(self):
        items = ItemModel.get_all_items()
        if len(items) == 0:
            return {"message": "no items in storage"}

        return {"all items": [ item.json() for item in items]}

        # return ItemModel.get_all_items()
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        #
        # result = []
        # for item in cursor.execute(query):
        #     el = {"name": item[0], "price": item[1]}
        #     result.append(el)
        # if len(result):
        #     connection.close()
        #     return {"items": result}
        #
        # connection.close()
        # return {"message": "no items in storage"}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",type=str, required=True, help="Fill the field")
    parser.add_argument("price",type=float, required=True, help="Fill the field")
    parser.add_argument("store_id",type=int, required=True, help="Every item need to have store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": f"no such item as {name}"}

    def post(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(request_data["name"])
        if item:
            return {"message": f"Item with name {request_data['name']} is alredy exsists"}, 400
        try:
            item = ItemModel(request_data["name"], request_data["price"], request_data["store_id"])
            item.save_to_db()
        except:
            return {"message": "error"}, 500 #internal server error


        return item.json(), 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": f"item {name} deleted"}
        else:
            return {"message": "not find"}
        # items = list(filter(lambda x: x["name"] != name, store["items"]))
        # item = ItemModel.find_by_name(name)
        # if item:
        #     connection = sqlite3.connect("data.db")
        #     cursor = connection.cursor()
        #     query = "DELETE FROM items WHERE name=?"
        #     cursor.execute(query, (name,))
        #     connection.commit()
        #     connection.close()
        #     return item.json()
        #     # return {"message": f"no {name} for deleting"}
        # #
        # # store["items"] = items
        # return {"message": f"no {name} for deleting"}


    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(data["name"])

        if item is None:
            item = ItemModel(data["name"], data["price"], data["store_id"])
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json()
