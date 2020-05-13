# app/medels/product.py
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from app import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    about = db.Column(db.String)
    price = db.Column(db.Float)
    category = db.Column(db.Integer)

    _loaded = False

    @property
    def str_price(self):
        return str(self.price)

    @str_price.setter
    def str_price(self, price):
        self.price = float(price)

    def save(self):
        if self.id != -1:
            db.session.add(self)
        db.session.commit()
        db.session.flush()

    @staticmethod
    def load(id=-1):
        if id != -1:
            return Product.query.filter_by(id=id).first()
        else:
            return Product()

    @staticmethod
    def load_all():
        result = Product.query.all()
        return result

    @staticmethod
    def delete(id):
        db.session.delete(Product.query.filter_by(id=id).first())
        db.session.commit()
