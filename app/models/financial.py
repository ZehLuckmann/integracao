# app/medels/financial.py
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from app import db


class Financial(db.Model):
    __tablename__ = "financial"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float)
    type = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    category = db.Column(db.String)

    _loaded = False

    def __init__(self, id=-1):
        if id != -1:
            self.id = id
        return

    @property
    def str_category(self):
        if self.category == 1:
            return "Saída"
        elif self.category == 2:
            return "Entrada"
        else:
            return "Desconhecida"

    @property
    def str_type(self):
        if self.category == 1:
            return "Evento"
        elif self.category == 2:
            return "Parceria"
        elif self.category == 3:
            return "Patrocínio"
        elif self.category == 4:
            return "Fornecedor"
        elif self.category == 5:
            return "Outros"
        else:
            return "Desconhecida"

    @property
    def str_value(self):
        return str(self.value)

    @str_value.setter
    def str_value(self, value):
        self.value = float(value)

    @property
    def str_date(self):
        if self.date:
            return datetime.datetime.strftime(self.date, '%Y-%m-%d')
        else:
            return False

    @str_date.setter
    def str_date(self, value):
        self.date = datetime.datetime.strptime(value, '%Y-%m-%d')

    def save(self):
        if self.id != -1:
            db.session.add(self)
        db.session.commit()
        db.session.flush()

    @staticmethod
    def load(id=-1):
        if id and id != -1:
            return Financial.query.filter_by(id=id).first()
        else:
            return Financial()

    @staticmethod
    def load_all():
        result = Financial.query.all()
        return result

    @staticmethod
    def delete(id):
        db.session.delete(Financial.query.filter_by(id=id).first())
        db.session.commit()
