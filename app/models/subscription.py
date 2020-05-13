# app/medels/subscription.py
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from app import db
from app.models.financial import Financial
from app.models.member import Member


class Subscription(db.Model):
    __tablename__ = "subscription"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    financial_id = db.Column(db.Integer, db.ForeignKey('financial.id'))
    plan = db.Column(db.String)    
    #value = db.Column(db.Float)

    _loaded = False

    @property
    def value(self):
        if self.plan == "socio junior":
            return 10
        elif self.plan == "socio pleno":
            return 20
        elif self.plan == "socio senior":
            return 30
        elif self.plan == "atleta":
            return 35
        elif self.plan == "formado":
            return 10
        elif self.plan == "diretoria":
            return 10
        elif self.plan == "agregado":
            return 25
        else:
            return 100

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
        print(self.date)
        if self.member_id != -1:
            member = Member.load(self.member_id)

            financial = Financial.load(self.financial_id)
            financial.date = self.date
            financial.value = self.value
            financial.description = "Assinatura {0} {1}".format(
                    member.name.title(),
                    self.plan.title())
            financial.type = "entrada"
            financial.category = "assinatura"
            financial.save()
            self.financial_id = financial.id

        if self.id != -1:
            db.session.add(self)
        db.session.commit()
        db.session.flush()

    @staticmethod
    def load(id=-1):
        if id != -1:
            return Subscription.query.filter_by(id=id).first()
        else:
            return Subscription()

    @staticmethod
    def load_member(member_id=-1):
        if member_id != -1:
            return Subscription.query.filter_by(member_id=member_id).all()
        else:
            return Subscription()


    @staticmethod
    def load_all():
        result = Subscription.query.all()
        return result

    @staticmethod
    def delete(id):
        subscription = Subscription.query.filter_by(id=id).first()        
        db.session.delete(subscription)        
        db.session.commit()
        Financial.delete(subscription.financial_id)

    @property
    def str_time(self):
        if self.time:
            return datetime.datetime.strftime(self.time, '%H:%M')
        else:
            return False

    @str_time.setter
    def str_time(self, value):
        self.time = datetime.datetime.strptime(value, '%H:%M')