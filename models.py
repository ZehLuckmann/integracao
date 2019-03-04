#coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from database import db

class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)
    nickname = db.Column(db.String)
    email = db.Column(db.String)
    adress = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    telephone = db.Column(db.String)
    about = db.Column(db.String)

    _loaded = False

    def save(self):
        if self.id != -1:
            db.session.add(self)
        db.session.commit()
        db.session.flush()

    @staticmethod
    def load(id=-1):
        if id != -1:
            print(id)
            return Member.query.filter_by(id=id).first()
        else:
            return Member()

    @staticmethod
    def load_all():
        result = Member.query.all()
        return result

    @staticmethod
    def delete(id):
        db.session.delete(Member.query.filter_by(id=id).first())
        db.session.commit()

class Financial(db.Model):
    __tablename__ = "financial"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float)
    type = db.Column(db.Integer)
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    category = db.Column(db.Integer)

    _loaded = False
    def __init__(self, id=-1):
        if id != -1:
            self.id=id
        return

    #GETTERS AND SETTERS
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
        self.value =float(value)

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


team_member = db.Table('team_member', db.Model.metadata,
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('member_id', db.Integer, db.ForeignKey('member.id'))
)
class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    members = db.relationship("Member",secondary=team_member)

    _loaded = False

    @property
    def member_count(self):
        return len(self.members)

    def save(self):
        if self.id != -1:
            db.session.add(self)
        db.session.commit()
        db.session.flush()

    @staticmethod
    def load(id=-1):
        if id != -1:
            return Team.query.filter_by(id=id).first()
        else:
            return Team()

    @staticmethod
    def load_all():
        result = Team.query.all()
        return result

    @staticmethod
    def delete(id):
        db.session.delete(Team.query.filter_by(id=id).first())
        db.session.commit()

    def add_member(self, member_id):
        self.members.append(Member.load(member_id))

    def delete_member(self, member_id):
        self.members.remove(Member.load(member_id))

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


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    category = db.Column(db.Integer)
    description = db.Column(db.String)

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