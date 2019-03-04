#coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
from application import app
from models.member import Member
from models.event import Event
from models.financial import Financial
from models.product import Product
from models.team import Team
from models.training import Training
import os
import datetime

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/calendar")
def calendar():
    events = Event.load_all()
    return render_template("calendar.html", events=events)