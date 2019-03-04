#coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from database import db

class Training(db.Model):
    __tablename__ = "training"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    _loaded = False

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
        if id != -1:
            return Training.query.filter_by(id=id).first()
        else:
            return Training()

    @staticmethod
    def load_team(team_id=-1):
        if team_id != -1:
            return Training.query.filter_by(team_id=team_id).all()
        else:
            return Training()


    @staticmethod
    def load_all():
        result = Training.query.all()
        return result

    @staticmethod
    def delete(id):
        db.session.delete(Training.query.filter_by(id=id).first())
        db.session.commit()
