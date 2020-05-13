# app/controllers/training.py
# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for
from app import app
from app.models.training import Training
from app.models.team import Team
import os
import datetime


@app.route("/training/edit/<int:team_id>")
@app.route("/training/edit/<int:team_id>/<int:training_id>",
           methods=['GET', 'POST'])
def edit_training(team_id, training_id=-1):
    team = Team.load(team_id)
    training = Training.load(training_id)
    return render_template("./team/edit_training.html", team=team, training=training)


@app.route("/training/save/<int:team_id>", methods=['GET', 'POST'])
@app.route("/training/save/<int:team_id>/<int:training_id>",
           methods=['GET', 'POST'])
def save_training(team_id, training_id=-1):
    if request.method == "POST":
               
        repeat = int(request.form.get("repeats"))
        days_interval = int(request.form.get("days_interval", 0))
        training_date = datetime.datetime.strptime(request.form.get("date"), '%Y-%m-%d')
        training_time = datetime.datetime.strptime(request.form.get("time"), '%H:%M')
        training_description = request.form.get("description")
        for i in range(repeat):
            training = Training.load(training_id)
            training.team_id = team_id
            training.date = training_date
            training.time = training_time
            training.description = training_description
            training.save()
            training_date += datetime.timedelta(days=days_interval)
        return redirect(url_for("list_training", team_id=team_id))

    training = Training.load(training_id)
    return redirect(url_for("edit_training", team_id=team_id, 
                    training=training))


@app.route("/training/list")
@app.route('/training/list/<int:team_id>')
def list_training(team_id=-1):
    if team_id == -1:
        trainings = Training.load_all()
    else:
        trainings = Training.load_team(team_id)

    team = Team.load(team_id)
    return render_template("./team/list_training.html", trainings=trainings,
                           team=team)


@app.route("/training/delete/<int:training_id>")
def delete_training(training_id):
    Training.delete(training_id)
    return redirect(url_for('list_training'))
