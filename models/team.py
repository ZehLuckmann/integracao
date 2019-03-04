#coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from database import db
from models.member import Member

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
