import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store = db.relationship("StoreModel")
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price, "store_id": self.store_id}

    @classmethod
    def find_by_name(cls, name):
        print('dasdas')
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return cls(*row)

        return None


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES(?, ?)"
        #
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()
    @classmethod
    def get_all_items(cls):
        # print(cls.query.all())
        # items = cls.query.all()
        # print(items[0].json())
        # for item in cls.query.all():
        #     print(item)

        return cls.query.all()



class ItemsListModel():
    pass
    # __tablename__ = "items"
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80))
    # price = db.Column(db.Float(precision=2))
    # @classmethod
    # def __init__(self, name, price):
    #     self.name = name
    #     self.price = price

    # @classmethod
    # def get_all_items(cls):
    #     return cls.query.all()
