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

#TEAM
@app.route("/team/edit")
@app.route("/team/edit/<int:team_id>", methods=['GET', 'POST'])
def edit_team(team_id=-1):
    team = Team.load(team_id)
    return render_template("edit_team.html", team=team)

@app.route("/team/save", methods=['GET', 'POST'])
@app.route("/team/save/<int:team_id>", methods=['GET', 'POST'])
def save_team(team_id=-1):
    if request.method == "POST":
        team = Team.load(team_id)
        team.description = request.form.get("description")
        team.save()

        return redirect(url_for("list_team"))

    return redirect(url_for("edit_team", team_id=team_id))

@app.route("/team/")
@app.route('/team/list')
def list_team():
    teams = Team.load_all()
    return render_template("list_team.html", teams=teams)


@app.route("/team/delete/<int:team_id>")
def delete_team(team_id):
    Team.delete(team_id)
    return redirect(url_for('list_team'))

@app.route("/team/member/edit")
@app.route("/team/member/edit/<int:team_id>", methods=['GET', 'POST'])
def edit_team_member(team_id=-1):
    team = Team.load(team_id)
    members = Member.load_all()
    return render_template("edit_team_member.html", team=team, members=members)

@app.route("/team/member/save/<int:team_id>", methods=['GET', 'POST'])
def save_team_member(team_id):
    if request.method == "POST":
        team = Team.load(team_id)
        team.add_member(int(request.form.get("team_member")))
        team.save()

        return redirect(url_for("edit_team_member", team_id=team_id))

    return redirect(url_for("edit_team_member", team_id=team_id))

@app.route("/team/member/delete/<int:team_id>/<int:member_id>")
def delete_team_member(team_id, member_id):
    team = Team.load(team_id)
    team.delete_member(member_id)
    return redirect(url_for('edit_team_member', team_id=team_id))