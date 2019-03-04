# app/controllers/event.py
# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for
from app import app
from app.models.event import Event
import os
import datetime


@app.route("/event/edit")
@app.route("/event/edit/<int:event_id>", methods=['GET', 'POST'])
def edit_event(event_id=-1):
    event = Event.load(event_id)
    return render_template("edit_event.html", event=event)


@app.route("/event/save", methods=['GET', 'POST'])
@app.route("/event/save/<int:event_id>", methods=['GET', 'POST'])
def save_event(event_id=-1):
    if request.method == "POST":
        event = Event.load(event_id)
        event.description = request.form.get("description")
        event.str_date = request.form.get("date")
        event.save()

        return redirect(url_for("list_event"))


@app.route("/event/")
@app.route('/event/list')
def list_event():
    events = Event.load_all()
    return render_template("list_event.html", events=events)


@app.route("/event/delete/<int:event_id>")
def delete_event(event_id):
    Event.delete(event_id)
    return redirect(url_for('list_event'))
