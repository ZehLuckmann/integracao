# app/controllers/defaults.py
# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for
from app import app
from app.models.event import Event
from app.models.training import Training
import os
import datetime


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/calendar")
def calendar():
    events = Event.load_all()
    trainings = Training.load_all()
    return render_template("./event/calendar.html", trainings=trainings, events=events)