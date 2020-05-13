# app/medels/event.py
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from app import db


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    category = db.Column(db.String)
    description = db.Column(db.String)

    _loaded = False

    @property
    def year_date(self):
        if self.date:
            return int(datetime.datetime.strftime(self.date, '%Y'))
        else:
            return False

    @property
    def month_date(self):
        if self.date:
            return int(datetime.datetime.strftime(self.date, '%m'))
        else:
            return False

    @property
    def day_date(self):
        if self.date:
            return int(datetime.datetime.strftime(self.date, '%d'))
        else:
            return False

    @property
    def str_date(self):
        if self.date:
            return datetime.datetime.strftime(self.date, '%Y-%m-%d')
        else:
            return False    

    @str_date.setter
    def str_date(self, value):
        self.date = datetime.datetime.strptime(value, '%Y-%m-%d')

    @property
    def str_time(self):
        if self.time:
            return datetime.datetime.strftime(self.time, '%H:%M')
        else:
            return False

    @str_time.setter
    def str_time(self, value):
        self.time = datetime.datetime.strptime(value, '%H:%M')
        
    def save(self):
        if self.id != -1:
            db.session.add(self)
        db.session.commit()
        db.session.flush()

    @staticmethod
    def load(id=-1):
        if id != -1:
            return Event.query.filter_by(id=id).first()
        else:
            return Event()

    @staticmethod
    def load_team(team_id=-1):
        if team_id != -1:
            return Event.query.filter_by(team_id=team_id).all()
        else:
            return Event()

    @staticmethod
    def load_all():
        result = Event.query.all()
        return result

    @staticmethod
    def delete(id):
        db.session.delete(Event.query.filter_by(id=id).first())
        db.session.commit()
        