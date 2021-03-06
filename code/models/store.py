import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name


    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):

        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        #
        # if row:
        #     return cls(*row)
        #
        # return None


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()


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
