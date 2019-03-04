# app/medels/member.py
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from app import db


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
