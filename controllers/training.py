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

@app.route("/training/edit/<int:team_id>")
@app.route("/training/edit/<int:team_id>/<int:training_id>", methods=['GET', 'POST'])
def edit_training(team_id, training_id=-1):
    team = Team.load(team_id)
    training = Training.load(training_id)
    return render_template("edit_training.html", team=team, training=training )


@app.route("/training/save/<int:team_id>", methods=['GET', 'POST'])
@app.route("/training/save/<int:team_id>/<int:training_id>", methods=['GET', 'POST'])
def save_training(team_id, training_id=-1):
    if request.method == "POST":
        training = Training.load(training_id)
        training.team_id = team_id
        training.str_date = request.form.get("date")
        training.save()

        return redirect(url_for("list_team"))

    training = Training.load(training_id)
    return redirect(url_for("edit_training", team_id=team_id, training=training))


@app.route("/training/list")
@app.route('/training/list/<int:team_id>')
def list_training(team_id=-1):
    if team_id == -1:
        trainings = Training.load_all()
    else:
        trainings = Training.load_team(team_id)

    team = Team.load(team_id)
    return render_template("list_training.html", trainings=trainings, team=team)

@app.route("/training/delete/<int:training_id>")
def delete_training(training_id):
    Training.delete(training_id)
    return redirect(url_for('list_training'))
